import logging
from os import environ

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from hash_retail.api import health, products, root, store
from hash_retail.schemas import ErrorResponse, InnerErrorResponse


def logging_setup() -> None:
    logfmt = "%(asctime)s | %(levelname)-8s | %(message)s   (%(filename)s:%(funcName)s)"
    datefmt = "%d/%m/%Y %H:%M:%S"

    log_levels_dict = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40}
    log_level = log_levels_dict[environ["API_LOGGING_LEVEL"]]

    # Create file and console logging handlers for the root logging
    logging.basicConfig(format=logfmt, datefmt=datefmt, level=log_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(fmt=logfmt, datefmt=datefmt))

    loggers = [
        logging.getLogger("gunicorn"),
        logging.getLogger("gunicorn.access"),
        logging.getLogger("gunicorn.error"),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("uvicorn.error"),
    ]

    for logger in loggers:
        logger.handlers = [console_handler]


def create_app() -> FastAPI:
    with open("VERSION.txt", "r", encoding="utf-8") as version_file:
        app_version = version_file.read().strip()

    shared_responses = {
        HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorResponse},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    }

    fastapi_app = FastAPI(
        title="Hash Challenge: E-Commerce Backend API",
        description=(
            "REST API for simulating retail checkouts using Python's FastAPI framework "
            "and consuming Hash's gRPC service for calculating product discounts."
        ),
        version=app_version,
        docs_url=None,
        redoc_url=None,
        responses=shared_responses,
    )

    fastapi_app.include_router(router=root.router, prefix="", include_in_schema=False)
    fastapi_app.include_router(
        router=health.router,
        prefix="/health",
        tags=["Health"],
    )
    fastapi_app.include_router(
        router=store.router,
        prefix="/store",
        tags=["Store"],
    )
    fastapi_app.include_router(
        router=products.router,
        prefix="/products",
        tags=["Products"],
    )

    @fastapi_app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        if 400 <= exc.status_code < 500:
            logging.info(exc.detail)
        elif exc.status_code >= 500:
            logging.exception(exc.detail)

        response = ErrorResponse(
            error=InnerErrorResponse(
                code=exc.status_code,
                message=str(exc.detail),
            )
        ).dict()
        return JSONResponse(content=response, status_code=exc.status_code)

    @fastapi_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        response = ErrorResponse(
            error=InnerErrorResponse(
                code=HTTP_422_UNPROCESSABLE_ENTITY,
                message=str(exc).replace("\n", ""),
            )
        ).dict()
        return JSONResponse(content=response, status_code=HTTP_422_UNPROCESSABLE_ENTITY)

    return fastapi_app
