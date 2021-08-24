from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import FileResponse
from starlette.responses import HTMLResponse, RedirectResponse

router = APIRouter()


@router.get("/favicon.ico")
async def favicon() -> FileResponse:
    return FileResponse("hash_retail/static/favicon.png")


@router.get("/docs", include_in_schema=False)
def overridden_swagger() -> HTMLResponse:
    url = router.url_path_for("favicon")
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Hash Challenge: E-Commerce Backend API",
        swagger_favicon_url=url,
    )


@router.get("/redoc", include_in_schema=False)
def overridden_redoc() -> HTMLResponse:
    url = router.url_path_for("favicon")
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Hash Challenge: E-Commerce Backend API",
        redoc_favicon_url=url,
    )


@router.get("/")
async def root() -> RedirectResponse:
    url = router.url_path_for("overridden_swagger")
    return RedirectResponse(url=url)
