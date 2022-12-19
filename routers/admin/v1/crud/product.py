from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from libs.utils import date, generate_id
from models import ProductModel
from routers.admin.v1.schemas import ProductBase


def add_product(db: Session, productSchema: ProductBase):
    db_product = ProductModel(
        id=generate_id(),
        product_name=productSchema.product_name,
        product_price=productSchema.product_price,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_id(db: Session, id: str):
    return (
        db.query(ProductModel)
        .filter(ProductModel.id == id, ProductModel.is_deleted == False)
        .first()
    )


def get_product(db: Session, id: str):
    db_product = get_product_by_id(db=db, id=id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return db_product


def get_products(db: Session, start: int, limit: int):
    db_product = (
        db.query(ProductModel)
        .filter(ProductModel.is_deleted == False)
        .offset(start)
        .limit(limit)
        .all()
    )
    return db_product


def update_product(db: Session, id: str, productSchema: ProductBase):
    db_product = get_product_by_id(db=db, id=id)
    db_product.product_price = productSchema.product_price
    db_product.updated_at = date()
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, id: str):
    db_product = get_product_by_id(db=db, id=id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    db_product.is_deleted = True
    db_product.updated_at = date()
    db.commit()
    db.refresh(db_product)
    print(db_product)
    return f"{db_product.product_name} is successfully deleted"
