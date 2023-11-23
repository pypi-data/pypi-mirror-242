try:
    import settings
    import deposit as deposit_system
except ImportError:
    import opcit.settings as settings
    import opcit.deposit as deposit_system

from fastapi import APIRouter, Request
from longsight.instrumentation import instrument
from starlette.responses import Response as StarletteResponse

router = APIRouter()


@router.post("/deposit/preserve/", tags=["deposit", "preservation"])
@instrument(
    create_aws=True,
    bucket=settings.BUCKET,
    sign_aws_requests=True,
    cloudwatch_push=True,
    log_group_name=settings.LOG_STREAM_GROUP,
    log_stream_name=settings.LOG_STREAM_NAME,
)
async def deposit(
    request: Request,
    instrumentation=None,
):
    return await deposit_system.OpCit(
        request=request, instrumentation=instrumentation
    ).process()
