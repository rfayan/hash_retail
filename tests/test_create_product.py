from json import dumps

from starlette import status

from hash_retail.core import product_dao
from hash_retail.models import Product as ProductModel
from hash_retail.schemas import Product as ProductSchema
from hash_retail.schemas import ProductBase


def test_create_product_success(mocker, client, db_session_mock):
    mocked_request = ProductBase(
        title="Interesting Title", description="A short description.", amount=9000, is_gift=False
    )
    mocked_product = ProductModel(id=1, **mocked_request.dict())
    expected_response = ProductSchema(id=1, **mocked_request.dict())

    mocker.patch.object(product_dao, "create_product", return_value=mocked_product)

    response = client.post("/products", data=mocked_request.json())

    product_dao.create_product.assert_called_once_with(db_session_mock, mocked_request)

    assert response.json() == expected_response
    assert response.status_code == status.HTTP_201_CREATED


def test_create_product_invalid_payload(mocker, client):
    mocked_request = dict(title="Interesting Title")

    mocker.patch.object(product_dao, "create_product", return_value=None)

    response = client.post("/products", data=dumps(mocked_request))

    product_dao.create_product.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response_error = response.json()["error"]

    assert "2 validation errors" in response_error["message"]
    assert "value_error.missing" in response_error["message"]
