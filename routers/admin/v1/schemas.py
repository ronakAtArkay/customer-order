from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    city: str = Field(..., min_length=1, max_length=50)
    mobile_number: str = Field(..., min_length=10, max_length=10)


class CustomerList(BaseModel):
    id: str
    name: str
    city: str
    mobile_number: str

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=50)
    product_price: str = Field(..., min_length=1, max_length=50)


class ProductList(BaseModel):
    id: str
    product_name: str
    product_price: str

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    customer_id: str = Field(..., min_length=36, max_length=36)
    product_id: str = Field(..., min_length=36, max_length=36)


class orderList(BaseModel):
    id: str
    customer: CustomerList
    product: ProductList

    class Config:
        orm_mode = True
