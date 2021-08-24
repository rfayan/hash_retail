from starlette import status


def test_swagger_docs_reachable(client):
    """Test if swagger documentation page is reachable."""
    response = client.get(url="/docs")

    assert response.status_code == status.HTTP_200_OK


def test_redoc_docs_reachable(client):
    """Test if ReDoc documentation page is reachable."""
    response = client.get("/redoc")

    assert response.status_code == status.HTTP_200_OK


def test_openapi_docs_reachable(client):
    """Test if OpenAPI specification is reachable."""
    response = client.get("/openapi.json")

    assert response.status_code == status.HTTP_200_OK
