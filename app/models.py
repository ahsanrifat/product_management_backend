# app/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# User Model
class User(Base):
    """
    SQLAlchemy model for a User.
    Represents a user in the e-commerce system.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False) # Added for admin role
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to orders made by this user
    orders = relationship("Order", back_populates="buyer")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"

# Product Model
class Product(Base):
    """
    SQLAlchemy model for a Product.
    Represents a product available for sale in the e-commerce system.
    Includes inventory details.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)  # Inventory quantity
    buying_price = Column(Float, nullable=False) # Cost to acquire the product
    selling_price = Column(Float, nullable=False) # Price at which it's sold
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to order items that include this product
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

# Order Model
class Order(Base):
    """
    SQLAlchemy model for an Order.
    Represents a customer's order, linking to the user and containing multiple order items.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending") # e.g., pending, completed, cancelled
    shipping_address = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to the user who placed the order
    buyer = relationship("User", back_populates="orders")
    # Relationship to the items within this order
    items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order(id={self.id}, buyer_id={self.buyer_id}, total_amount={self.total_amount})>"

# OrderItem Model
class OrderItem(Base):
    """
    SQLAlchemy model for an Order Item.
    Represents a specific product within an order, with its quantity and price at the time of purchase.
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False) # Price of the product when it was bought
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships to the parent order and the product
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"

