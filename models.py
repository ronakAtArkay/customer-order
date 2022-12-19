import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class CoustomerModel(Base):
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, default=None)
    city = Column(String(255), nullable=False, default=None)
    mobile_number = Column(String(15), unique=True, nullable=True, default=None)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True)
    product_name = Column(String(255), nullable=False, default=None)
    product_price = Column(String(10), nullable=False, default=None)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

    customer = relationship("CoustomerModel", backref="orders")
    product = relationship("ProductModel", backref="orders")
