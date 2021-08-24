from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from hash_retail import models, schemas
from hash_retail.core import product_dao
from hash_retail.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.Product], response_model_exclude_unset=True)
def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[models.Product]:
    products = product_dao.list_products(db, skip=skip, limit=limit)
    return products


@router.post("", status_code=HTTP_201_CREATED, response_model=schemas.Product)
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)) -> models.Product:
    try:
        return product_dao.create_product(db, product)
    except Exception as err:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(err)) from err


@router.get(
    "/{product_id}",
    response_model=schemas.Product,
    response_model_exclude_unset=True,
    responses={HTTP_404_NOT_FOUND: {"model": schemas.ErrorResponse}},
)
def get_product(product_id: int, db: Session = Depends(get_db)) -> models.Product:
    db_product = product_dao.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found"
        )
    return db_product


@router.delete(
    "/{product_id}",
    status_code=HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={HTTP_404_NOT_FOUND: {"model": schemas.ErrorResponse}},
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> None:
    db_product = product_dao.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found"
        )

    product_dao.delete_product(db, product_id=product_id)
