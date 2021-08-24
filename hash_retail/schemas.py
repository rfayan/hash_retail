from typing import List

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    title: str = Field(..., description="Title of the product")
    description: str = Field("", description="Detailed description of the product")
    amount: int = Field(..., ge=1, description="Price of each product unit")
    is_gift: bool = Field(..., description="If product can be given as a free gift")


class Product(ProductBase):
    id: int = Field(..., description="Product ID")

    class Config:
        orm_mode = True


class ProductRequest(BaseModel):
    id: int = Field(..., description="Product ID")
    quantity: int = Field(..., ge=1, description="Quantity of products of this same ID")


class ProductResponse(ProductRequest):
    unit_amount: int = Field(..., description="Price of each product unit")
    total_amount: int = Field(..., description="Total price for this product ID")
    discount: int = Field(..., description="Total discount given for this product ID")
    is_gift: bool = Field(..., description="If product was given as a free gift")


class CheckoutRequest(BaseModel):
    products: List[ProductRequest] = Field(
        ..., min_items=1, description="List of products to be checked out"
    )


class CheckoutResponse(BaseModel):
    total_amount: int = Field(..., description="Total price without discounts")
    total_amount_with_discount: int = Field(..., description="Total price with discounts")
    total_discount: int = Field(..., description="Total discount")
    products: List[ProductResponse] = Field(
        ..., description="List of products with pricing information"
    )


class InnerErrorResponse(BaseModel):
    """Inner Model for Error Response."""

    code: int = Field(..., description="HTTP response code of the error", example=404)
    message: str = Field(..., description="Error message description", example="Product not found")


class ErrorResponse(BaseModel):
    """Data Model class for marshalling generic error responses."""

    error: InnerErrorResponse = Field(..., description="Error description")
