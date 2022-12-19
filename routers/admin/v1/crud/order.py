from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from libs.utils import date, generate_id
from models import CoustomerModel, OrderModel, ProductModel
from routers.admin.v1.schemas import OrderBase


def add_order(orderSchema: OrderBase, db: Session):
    db_order = OrderModel(
        id=generate_id(),
        customer_id=orderSchema.customer_id,
        product_id=orderSchema.product_id,
    )
    # customer_id = db.query(CoustomerModel).filter(CoustomerModel.id == orderSchema.customer_id).first()
    # product_id = db.query(ProductModel).filter(ProductModel.id == orderSchema.product_id).first()
    verify_id = (
        db.query(CoustomerModel, ProductModel)
        .filter(
            CoustomerModel.id == orderSchema.customer_id,
            ProductModel.id == orderSchema.product_id,
        )
        .first()
    )
    if verify_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id not found"
        )
    # if product_id is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_by_id(id: str, db: Session):
    return (
        db.query(OrderModel)
        .filter(OrderModel.id == id, OrderModel.is_deleted == False)
        .first()
    )


def get_order(id: str, db: Session):
    db_order = get_order_by_id(id=id, db=db)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return db_order


def get_orders(start: int, limit: int, db: Session):
    db_order = (
        db.query(OrderModel)
        .filter(OrderModel.is_deleted == False)
        .offset(start)
        .limit(limit)
        .all()
    )
    return db_order


def update_order(id: str, orderSchema: OrderBase, db: Session):
    db_order = get_order_by_id(id=id, db=db)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    db_order.product_id = orderSchema.product_id
    db_order.updated_at = date()
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(id: str, db: Session):
    db_order = get_order_by_id(id=id, db=db)
    customer_name = (
        db.query(CoustomerModel)
        .join(OrderModel)
        .filter(OrderModel.customer_id == CoustomerModel.id)
        .first()
    )
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    db_order.is_deleted = True
    db_order.updated_at = date()
    db.commit()
    db.refresh(db_order)
    return f"{customer_name.name} your order deleted successfully"
