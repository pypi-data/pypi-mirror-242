import io

import clannotation.annotator
import claws.aws_utils
from internetarchive import get_session, upload, modify_metadata, ArchiveSession
import magic

try:
    import settings
except ImportError:
    import opcit.settings as settings


class Archive:
    def __init__(self, log_function):
        self.log_function = log_function
        self.archive_name = "Internet Archive"

    def deposit(
        self,
        file_object: bytes,
        warnings: list,
        doi: str,
        metadata: dict = None,
    ) -> list:
        """
        Deposit a file to the archive
        :param metadata:
        :param doi: the DOIs
        :param warnings: the warnings dictionary
        :param file_object: the file objects to deposit
        :return: None
        """
        self.log_function(f"Invoking {self.archive_name} depositor")

        mime_proceed, mime_type = self._check_mimes(file_object, warnings)

        if not mime_proceed:
            return warnings

        ia_session = self._get_ia_session()

        test_metadata = {
            "title": metadata["title"],
            "authors": metadata["authors"],
            "date": metadata["date"],
            "doi": doi,
        }

        remote_file = clannotation.annotator.Annotator.doi_to_md5(doi)
        ia_item = ia_session.get_item(remote_file)

        r = ia_item.upload(files=file_object, metadata=test_metadata)

        return warnings

    def _check_mimes(
        self, file_object: bytes, warnings: list
    ) -> tuple[bool, list]:
        """
        Check the MIME type of the file
        :param file_object: the file object to check
        :param warnings: the warnings list
        :return: tuple of bool for success and list of warnings
        """
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(file_object)

        self.log_function(f"File MIME type is {mime_type}")

        if mime_type != "application/pdf":
            warnings.append(
                f"File MIME type is {mime_type}. "
                "This item will not be archived as only PDF is supported."
            )
            return False, warnings
        else:
            return True, warnings

    @staticmethod
    def _get_ia_session() -> ArchiveSession:
        """
        Get an Internet Archive session
        :return: the session
        """
        config = {
            "s3": {
                "access": settings.ACCESS_KEY["access_key"],
                "secret": settings.ACCESS_KEY["secret_key"],
            }
        }
        ia_session = get_session(config=config)
        return ia_session
