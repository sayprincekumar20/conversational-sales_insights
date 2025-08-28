from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"
    CustomerID = Column(String, primary_key=True)
    CompanyName = Column(String)
    ContactName = Column(String)
    Region = Column(String)


# class Category(Base):
#     __tablename__ = "categories"
#     CategoryID = Column(Integer, primary_key=True)
#     CategoryName = Column(String)


# class Product(Base):
#     __tablename__ = "products"
#     ProductID = Column(Integer, primary_key=True)
#     ProductName = Column(String)
#     CategoryID = Column(Integer, ForeignKey("categories.CategoryID"))
#     category = relationship("Category")


# class Order(Base):
#     __tablename__ = "orders"
#     OrderID = Column(Integer, primary_key=True)
#     CustomerID = Column(String, ForeignKey("customers.CustomerID"))
#     OrderDate = Column(DateTime)
#     ShipRegion = Column(String)
#     customer = relationship("Customer")


# class OrderDetail(Base):
#     __tablename__ = "order_details"
#     OrderID = Column(Integer, ForeignKey("orders.OrderID"), primary_key=True)
#     ProductID = Column(Integer, ForeignKey("products.ProductID"), primary_key=True)
#     UnitPrice = Column(Float)
#     Quantity = Column(Integer)
#     product = relationship("Product")
#     order = relationship("Order")