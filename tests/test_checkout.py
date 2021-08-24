import pytest
from starlette import status

from hash_retail.api import store
from hash_retail.core import product_dao
from hash_retail.models import Product as ProductModel
from hash_retail.schemas import CheckoutRequest, ProductRequest


@pytest.mark.parametrize(
    "discount_percentage, black_friday, expected_total",
    [
        (0, False, 10000),
        (0.05, False, 9500),
        (0, True, 10000),
        (0.05, True, 9500),
    ],
)
def test_checkout(
    mocker, client, db_session_mock, discount_percentage, black_friday, expected_total
):
    mocked_product_id = 1
    mocked_product_quantity = 2
    mocked_product_amount = 5000

    mocked_request = CheckoutRequest(
        products=[ProductRequest(id=mocked_product_id, quantity=mocked_product_quantity)]
    )
    mocked_product = ProductModel(
        id=mocked_product_id,
        title="Interesting Title",
        description="A short description.",
        amount=mocked_product_amount,
        is_gift=False,
    )
    mocked_gift_product = ProductModel(
        id=6, title="Gift Title", description="This is a gift.", amount=42, is_gift=True
    )

    mocker.patch.object(product_dao, "get_product", return_value=mocked_product)
    mocker.patch.object(product_dao, "get_gift_product", return_value=mocked_gift_product)
    mocker.patch.object(store, "get_discount_percentage", return_value=discount_percentage)
    mocker.patch.object(store, "is_black_friday", return_value=black_friday)

    response = client.post("/store/checkout", data=mocked_request.json())

    assert response.status_code == status.HTTP_200_OK

    product_dao.get_product.assert_called_once_with(db_session_mock, mocked_product_id)
    store.get_discount_percentage.assert_called_once_with(mocked_product_id)
    store.is_black_friday.assert_called_once_with()

    response_dict = response.json()

    assert response_dict["total_amount_with_discount"] == expected_total

    if black_friday:
        assert len(response_dict["products"]) == 2  # Free gift product on black friday
    else:
        assert len(response_dict["products"]) == 1  # No gift (only 1 unique product)
