import asyncio
import datetime
import re
from importlib import import_module
from pathlib import Path

import httpx
from fastapi import HTTPException, Request, Response, UploadFile
from lxml import etree
from lxml.etree import Element

try:
    import settings
except ImportError:
    import opcit.settings as settings


class OpCit:
    def __init__(
        self,
        request: Request,
        instrumentation=None,
    ):
        self.request = request
        self.instrumentation = instrumentation

    async def process(self) -> Response:
        warnings = []

        # extract the details and make sure they are a valid Crossref metadata
        # deposit request
        file, login_id, login_password = await self._validate_request(
            self.request
        )

        self.log("Request validated")

        etree_parsed, namespace = self._etree_and_namespace(file)

        if not self._validate_xml_against_schema(parsed_xml=etree_parsed):
            self.log("Invalid XML submitted (does not conform to 5.3.1)")
            return Response(
                content="Invalid XML",
                status_code=400,
            )

        # if we get here, then the document is valid
        self.log("XML is valid 5.3.1 schema")

        # now look for DOIs
        dois: list[Element] = self._extract_dois(etree_parsed)
        self.log(f"Found {len(dois)} DOIs for processing")

        for doi in dois:
            # first, find the parent journal_article element
            journal_article: Element = doi.getparent()

            while (
                journal_article is not None
                and not journal_article.tag.endswith("journal_article")
            ):
                journal_article: Element = journal_article.getparent()

                if journal_article is None:
                    break

            if journal_article is None:
                # top of the tree
                # error out
                self.log(f"{doi.text} is not a journal DOI")
                warnings.append(f"{doi.text} is not a journal DOI")
                continue

            # now look for open licensing information to check that
            # we have permission to archive
            license_ref, license_regex = await self._extract_license(
                journal_article
            )

            # Extract and print the text content of the found license_ref
            # element
            if (
                license_ref
                and re.match(license_regex, license_ref[0].text) is not None
            ):
                self.log("License is a valid CC license")

                resource = await self._extract_fulltext(journal_article)

                if len(resource) > 0:
                    remote_file = resource[0].text

                    try:
                        self.log(f"Fetching {remote_file}")
                        file_object = await OpCit._fetch_url(url=remote_file)
                        self.log(f"Fetched {remote_file}")
                    except Exception as e:
                        self.log(f"Error fetching {remote_file}: {e}")
                        warnings.append(
                            f"Error fetching {remote_file}: {e}. "
                            "This item will not be archived."
                        )
                        file_object = None

                    if file_object:
                        # extract authors
                        # there are some Western naming assumptions going on
                        # here that should be corrected
                        authors = await self._extract_authors(journal_article)

                        # extract the title
                        title = await self._extract_title(journal_article)

                        # extract the date
                        date = await self._extract_date(journal_article)

                        for (
                            depositor_name,
                            depositor_module,
                        ) in settings.DEPOSIT_SYSTEMS.items():
                            # temporary block
                            return

                            self.deposit(
                                depositor_name=depositor_name,
                                depositor_module=depositor_module,
                                file_object=file_object[0],
                                warnings=warnings,
                                doi=doi.text,
                            )
                else:
                    self.log("No resource found")
                    warnings.append(
                        "No resource found. This item will not be archived."
                    )
            else:
                self.log("License is not a valid CC license")
                warnings.append(
                    "License is not a valid CC license. "
                    "This item will not be archived."
                )

        response = Response(content="Welcome to Op Cit")
        return response

    @staticmethod
    async def _extract_date(journal_article):
        date_block: list[Element] = journal_article.xpath(
            ".//publication_date",
            namespaces={"xmlns": "http://www.crossref.org/schema/5.3.1"},
        )

        date_object = datetime.date(
            year=int(
                journal_article.xpath(
                    ".//xmlns:publication_date/xmlns:year",
                    namespaces={
                        "xmlns": "http://www.crossref.org/schema/5.3.1"
                    },
                )[0].text
            ),
            month=int(
                journal_article.xpath(
                    ".//xmlns:publication_date/xmlns:month",
                    namespaces={
                        "xmlns": "http://www.crossref.org/schema/5.3.1"
                    },
                )[0].text
            ),
            day=int(
                journal_article.xpath(
                    ".//xmlns:publication_date/xmlns:day",
                    namespaces={
                        "xmlns": "http://www.crossref.org/schema/5.3.1"
                    },
                )[0].text
            ),
        )

        return date_object

    @staticmethod
    async def _extract_title(journal_article):
        titles: list[Element] = journal_article.xpath(
            ".//xmlns:titles/xmlns:title",
            namespaces={"xmlns": "http://www.crossref.org/schema/5.3.1"},
        )

        return titles[0].text

    @staticmethod
    async def _extract_authors(journal_article):
        contributors: list[Element] = journal_article.xpath(
            ".//xmlns:contributors/*[@contributor_role = 'author']",
            namespaces={"xmlns": "http://www.crossref.org/schema/5.3.1"},
        )

        authors = []

        for contributor in contributors:
            if contributor.tag.endswith("person_name"):
                author = {
                    "given_name": contributor.xpath(
                        ".//xmlns:given_name",
                        namespaces={
                            "xmlns": "http://www.crossref.org/schema/5.3.1"
                        },
                    )[0].text,
                    "surname": contributor.xpath(
                        ".//xmlns:surname",
                        namespaces={
                            "xmlns": "http://www.crossref.org/schema/5.3.1"
                        },
                    )[0].text,
                }

                is_first = contributor.xpath(
                    ".//@sequence[.='first']",
                    namespaces={
                        "xmlns": "http://www.crossref.org/schema/5.3.1"
                    },
                )

                authenticated_orcid = contributor.xpath(
                    ".//xmlns:ORCID[@authenticated='true']",
                    namespaces={
                        "xmlns": "http://www.crossref.org/schema/5.3.1"
                    },
                )

                if authenticated_orcid:
                    author["ORCID"] = authenticated_orcid[0].text

                if is_first:
                    authors.insert(0, author)
                else:
                    authors.append(author)

        return authors

    @staticmethod
    async def _extract_fulltext(journal_article):
        resource: list[Element] = journal_article.xpath(
            './/xmlns:collection[@property="crawler-based"]/xmlns:item'
            '[@crawler="iParadigms"]/xmlns:resource',
            namespaces={"xmlns": "http://www.crossref.org/schema/5.3.1"},
        )
        return resource

    @staticmethod
    async def _extract_license(journal_article):
        # <license_ref applies_to="vor" start_date="2008-08-13">
        # http://creativecommons.org/licenses/by/3.0/deed.en_US</license_ref>
        license_regex = r"^https?://creativecommons.org/licenses/.+"
        license_element = "license_ref"
        necessary_applies_to = "vor"
        license_ref = journal_article.xpath(
            f'//xmlns:{license_element}[@applies_to="'
            f'{necessary_applies_to}"]',
            namespaces={
                "xmlns": "http://www.crossref.org/AccessIndicators.xsd"
            },
        )
        return license_ref, license_regex

    def _extract_dois(self, parsed_xml) -> list[Element]:
        crossref_namespace = self._extract_namespace(parsed_xml)
        namespaces = {"crossref": crossref_namespace}

        doi_data_elements = parsed_xml.findall(
            f"//crossref:doi_data/crossref:doi", namespaces=namespaces
        )
        return doi_data_elements

    def deposit(
        self,
        depositor_name,
        depositor_module,
        file_object,
        warnings: list,
        doi,
    ):
        """
        Deposit a file in an archive
        :param doi: the DOI
        :param warnings: the warnings list
        :param depositor_name: the name
        :param depositor_module: depositor module string
        :param file_object: the file object to deposit
        :return: None
        """
        self.log(f"Loading module {depositor_name}")
        process_module = import_module(f"depositors.{depositor_module}")

        archive = process_module.Archive(self.log)
        archive.deposit(file_object=file_object, warnings=warnings, doi=doi)

    def log(self, message) -> None:
        """
        Log a message
        :param message: the message to log
        :return: None
        """
        if self.instrumentation:
            self.instrumentation.logger.info(message)

    @staticmethod
    async def _make_request(client: httpx.AsyncClient, url: str) -> bytes:
        """
        Make a remote request
        :param client: the client object
        :param url: the URL to request
        :return: the response
        """
        response = await client.get(url)

        return response.content

    @staticmethod
    async def _fetch_url(url) -> tuple[bytes]:
        """
        Fetch a remote URL
        :param url: the URL to fetch
        :return: list of async task responses
        """
        async with httpx.AsyncClient() as client:
            tasks = [OpCit._make_request(client, url)]
            result = await asyncio.gather(*tasks)
            return result

    @staticmethod
    async def _validate_request(request) -> tuple[UploadFile, str, str]:
        """
        Check that this is a valid deposit request and extract the needed info
        :param request: the current request
        :return: a tuple of the submitted file, login_id, and login_passwd
        """
        # 1. check that the content type of this request is
        #  "multipart/form-data"
        # 2. check that the following parameters are all set:
        # a. login_id, the depositing username and/or role in format user/role
        #  or role
        # b. login_passwd, the depositing user password
        # c. operation, the value should be “doMDUpload”.
        # 3. extract the file from the request (in the "files" parameter)

        content_type = request.headers.get("content-type")
        if content_type.startswith("multipart/form-data"):
            form = await request.form()

            if (
                "login_id" in form
                and "login_passwd" in form
                and "operation" in form
            ):
                if form["operation"] == "doMDUpload":
                    if "mdFile" in form:
                        return (
                            form["mdFile"],
                            form["login_id"],
                            form["login_passwd"],
                        )
                    else:
                        raise HTTPException(
                            status_code=400,
                            detail="Missing 'mdFile' field in the request.",
                        )
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid value for 'operation'. "
                        "Must be 'doMDUpload'.",
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Missing required parameters "
                    "(login_id, login_passwd, operation).",
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid content type. Must be 'multipart/form-data'.",
            )

    @staticmethod
    def _validate_xml_against_schema(
        parsed_xml,
        base_url="",
        reload=False,
    ) -> tuple[etree, bool, etree]:
        """
        Validate the XML against the schema
        :param parsed_xml: the parsed XML
        :param base_url: the base URL
        :param reload: whether to reload the XML
        :return: tuple of etree, is_valid, parsed_xml
        """
        # TODO: this must select the right XSD file

        xsd_file = Path(f"depositor_schema/5.3.1/crossref5.3.1.xsd")

        xml_element_tree = parsed_xml

        if base_url:
            xsd_tree = etree.parse(
                xsd_file, base_url=base_url if base_url else None
            )
        else:
            xsd_tree = etree.parse(xsd_file)

        if reload:
            # reparse
            xml_element_tree = etree.fromstring(
                etree.tostring(xml_element_tree)
            )

        xml_schema = etree.XMLSchema(xsd_tree)
        is_valid = xml_schema.validate(xml_element_tree)

        return etree, is_valid, parsed_xml

    def _etree_and_namespace(self, file) -> tuple[etree, str]:
        """
        Parse the XML and extract the namespace
        :param file: the file to parse
        :return: tuple of etree and namespace
        """
        # validate the XML against the schema
        from lxml import etree

        parsed_xml = etree.parse(file.file)

        return parsed_xml, self._extract_namespace(parsed_xml)

    @staticmethod
    def _extract_namespace(
        tree, namespace: str = None, namespace_mode=False
    ) -> str:
        """
        Extract the namespace from an XML tree.
        :param tree: the XML tree
        :param namespace: the namespace or None
        :param namespace_mode: whether to return the namespace or the URL
        :return: the namespace
        """

        if namespace is None:
            return tree.xpath(f"namespace-uri(.)")

        else:
            ns_select = (
                "//namespace::*[not(. = "
                "'http://www.w3.org/XML/1998/namespace') "
                "and . = namespace-uri(..)]"
            )

            for ns, url in tree.xpath(ns_select):
                if not namespace_mode:
                    if ns == namespace:
                        return url
                else:
                    if url == namespace:
                        return ns
