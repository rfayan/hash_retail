"""Product DAO (Data Access Object) interface for interacting with the database."""

from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from hash_retail import models, schemas


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_gift_product(db: Session) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.is_gift).order_by(func.random()).first()


def list_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductBase) -> models.Product:
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> None:
    db_product = get_product(db, product_id)
    db.delete(db_product)
    db.commit()


def update_product(db: Session, product_id: int, **kwargs: str) -> None:
    db_product = get_product(db, product_id)

    # For each key-value pair, update the product DB object with the given new attribute value
    for attribute, new_value in kwargs.items():
        setattr(db_product, attribute, new_value)

    db.commit()
