from sqlalchemy import inspect
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


def get_all_orders(db: Session):
    db_order = db.query(OrderModel).filter(OrderModel.is_deleted == False).all()
    return db_order


def update_order(id: str, orderSchema: OrderBase, db: Session):
    db_order = get_order_by_id(id=id, db=db)
    verify_id = (
        db.query(ProductModel)
        .filter(
            ProductModel.id == orderSchema.product_id,
        )
        .first()
    )
    if verify_id is None:
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
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    print(object_as_dict(db_order.customer))
    db_order.is_deleted = True
    db_order.updated_at = date()
    db.commit()
    db.refresh(db_order)

    return f"{db_order.customer.name} your order is deleted successfully"



def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
    