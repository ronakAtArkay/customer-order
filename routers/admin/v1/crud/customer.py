from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from libs.utils import date, generate_id
from models import CoustomerModel
from routers.admin.v1.schemas import CustomerBase


def add_customer(db: Session, customerSchema: CustomerBase):
    db_customer = CoustomerModel(
        id=generate_id(),
        name=customerSchema.name,
        city=customerSchema.city,
        mobile_number=customerSchema.mobile_number,
    )
    print(type(db_customer))
    db_number = (
        db.query(CoustomerModel)
        .filter(CoustomerModel.mobile_number == customerSchema.mobile_number)
        .first()
    )
    # print(db_number.mobile_number)
    if db_customer.mobile_number == db_number:
        raise HTTPException(
            status_code=status.HTTP_208_ALREADY_REPORTED,
            detail="customer are already created",
        )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customer_by_id(db: Session, id: str):
    return (
        db.query(CoustomerModel)
        .filter(CoustomerModel.id == id, CoustomerModel.is_deleted == False)
        .first()
    )


def get_customer(db: Session, id: str):
    db_customer = get_customer_by_id(db=db, id=id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="coustomer not found"
        )
    return db_customer


def get_customers(db: Session, start: int, limit: str):
    db_customer = (
        db.query(CoustomerModel)
        .filter(CoustomerModel.is_deleted == False)
        .offset(start)
        .limit(limit)
        .all()
    )
    return db_customer


def update_customer(db: Session, id: str, customerSchema: CustomerBase):
    db_customer = get_customer_by_id(db=db, id=id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="customer not found"
        )
    db_customer.name = customerSchema.name
    db_customer.city = customerSchema.city
    db_customer.mobile_number = customerSchema.mobile_number
    db_customer.updated_at = date()
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, id: str):
    db_customer = get_customer_by_id(db=db, id=id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="customer not found"
        )
    db_customer.is_deleted = True
    db_customer.updated_at = date()
    db.commit()
    db.refresh(db_customer)
    return f"{db_customer.name} is successfully deleted"
