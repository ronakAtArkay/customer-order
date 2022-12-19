from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from dependencies import get_db
from routers.admin.v1.crud import customer, order, product
from routers.admin.v1.schemas import (
    CustomerBase,
    CustomerList,
    OrderBase,
    ProductBase,
    ProductList,
    orderList,
)

router = APIRouter()

# start customer


@router.post("/customer", response_model=CustomerList, tags=["customer"])
def add_customer(customerSchema: CustomerBase, db: Session = Depends(get_db)):
    data = customer.add_customer(customerSchema=customerSchema, db=db)
    return data


@router.get("/customers/{id}", response_model=CustomerList, tags=["customer"])
def get_customer(
    id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = customer.get_customer(id=id, db=db)
    return data


@router.get("/customers", response_model=List[CustomerList], tags=["customer"])
def get_customers(start: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    data = customer.get_customers(start=start, limit=limit, db=db)
    return data


@router.put("/customers/{id}", tags=["customer"])
def update_customer(
    customerSchema: CustomerBase,
    id: str = Path(min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    data = customer.update_customer(id=id, customerSchema=customerSchema, db=db)
    return data


@router.delete("/customers/{id}", tags=["customer"])
def delete_customer(
    id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = customer.delete_customer(id=id, db=db)
    return data


# end customer

# start product


@router.post("/product", response_model=ProductList, tags=["product"])
def add_product(productSchema: ProductBase, db: Session = Depends(get_db)):
    data = product.add_product(productSchema=productSchema, db=db)
    return data


@router.get("/product/{id}", response_model=ProductList, tags=["product"])
def get_product(
    id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = product.get_product(id=id, db=db)
    return data


@router.get("/products", response_model=List[ProductList], tags=["product"])
def get_products(start: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    data = product.get_products(start=start, limit=limit, db=db)
    return data


@router.put("/product/{id}", response_model=ProductList, tags=["product"])
def update_product(
    productSchema: ProductBase,
    id: str = Path(min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    data = product.update_product(productSchema=productSchema, id=id, db=db)
    return data


@router.delete("/product/{id}", tags=["product"])
def delete_product(
    id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = product.delete_product(id=id, db=db)
    return data


# end product

# start order


@router.post("/order", response_model=orderList, tags=["customer-order"])
def add_order(orderSchema: OrderBase, db: Session = Depends(get_db)):
    data = order.add_order(orderSchema=orderSchema, db=db)
    return data


@router.get("/order/{id}", response_model=orderList, tags=["customer-order"])
def get_order(
    id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = order.get_order(id=id, db=db)
    return data


@router.get("/orders", response_model=List[orderList], tags=["customer-order"])
def get_orders(start: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    data = order.get_orders(start=start, limit=limit, db=db)
    return data


@router.put("/order/{id}", response_model=orderList, tags=["customer-order"])
def update_order(orderSchema: OrderBase,id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)):
    data = order.update_order(id=id, orderSchema=orderSchema, db=db)
    return data


@router.delete("/order/{id}", tags=["customer-order"])
def delete_order(id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)):
    data = order.delete_order(id=id, db=db)
    return data
