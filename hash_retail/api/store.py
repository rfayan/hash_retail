import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from hash_retail import schemas
from hash_retail.core import product_dao
from hash_retail.core.black_friday import is_black_friday
from hash_retail.core.grpc.discount import get_discount_percentage
from hash_retail.database import get_db
from hash_retail.schemas import CheckoutRequest, CheckoutResponse, ProductResponse

router = APIRouter()


@router.post(
    "/checkout",
    status_code=HTTP_200_OK,
    response_model=CheckoutResponse,
    responses={HTTP_404_NOT_FOUND: {"model": schemas.ErrorResponse}},
)
async def checkout(request: CheckoutRequest, db: Session = Depends(get_db)) -> CheckoutResponse:
    products_response = []
    products_request = request.products

    total_amount_sum = 0
    total_discount_sum = 0

    for product in products_request:
        product_model = product_dao.get_product(db, product.id)

        if product_model is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail=f"Product {product.id} not found"
            )

        total_amount = product_model.amount * product.quantity
        discount_percentage = await get_discount_percentage(product_model.id)
        discount = int(discount_percentage * total_amount)

        logging.debug("Total discount for product %s: %s", product_model.id, discount)

        total_amount_sum += total_amount
        total_discount_sum += discount

        product_dict = ProductResponse(
            id=product_model.id,
            quantity=product.quantity,
            unit_amount=product_model.amount,
            total_amount=total_amount,
            discount=discount,
            is_gift=False,
        )

        products_response.append(product_dict)

    if is_black_friday():
        logging.debug("Free Black Friday gift!")

        gift_product_model = product_dao.get_gift_product(db)
        gift_product_dict = ProductResponse(
            id=gift_product_model.id,
            quantity=1,
            unit_amount=0,
            total_amount=0,
            discount=0,
            is_gift=True,
        )

        products_response.append(gift_product_dict)

    return CheckoutResponse(
        total_amount=total_amount_sum,
        total_amount_with_discount=total_amount_sum - total_discount_sum,
        total_discount=total_discount_sum,
        products=products_response,
    )
