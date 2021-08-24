from sqlalchemy import Boolean, Column, Integer, String

from hash_retail.database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Integer, nullable=False)
    is_gift = Column(Boolean, nullable=False)
