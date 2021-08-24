from fastapi import APIRouter, Response
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter()


@router.get("/liveness", status_code=HTTP_204_NO_CONTENT, response_class=Response)
def api_liveness() -> None:
    """Endpoint to check if API is running (liveness)."""


@router.get("/readiness", status_code=HTTP_204_NO_CONTENT, response_class=Response)
def api_readiness() -> None:
    """Endpoint to check if API is ready to be consumed (readiness)."""
    # TODO: Check external dependencies and backend load
