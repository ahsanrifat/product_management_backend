# app/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional,List
from . import models, schemas
from .auth import get_password_hash # Import the password hashing utility

# --- User CRUD Operations ---

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Retrieve a user by their ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Retrieve a user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Retrieve a list of users with pagination."""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user with a hashed password."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        phone_number=user.phone_number,
        address=user.address,
        is_admin=user.is_admin # Set admin status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """Update an existing user's information."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True) # Use model_dump for Pydantic v2
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    """Delete a user by their ID."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# --- Product CRUD Operations ---

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Retrieve a product by its ID."""
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """Retrieve a list of products with pagination."""
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """Create a new product."""
    db_product = models.Product(**product.model_dump()) # Use model_dump for Pydantic v2
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate) -> Optional[models.Product]:
    """Update an existing product's information."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True) # Use model_dump for Pydantic v2
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Delete a product by its ID."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# --- Order CRUD Operations ---

def create_user_order(db: Session, order: schemas.OrderCreate, buyer_id: int) -> models.Order:
    """
    Create a new order for a user.
    This function handles deducting product quantities and calculating total amount.
    """
    total_amount = 0
    db_order_items = []

    for item_in in order.items:
        product = get_product(db, item_in.product_id)
        if not product or product.quantity < item_in.quantity:
            # You might want to raise an HTTPException here in the router
            # For CRUD, we'll return None or handle it as an error.
            raise ValueError(f"Product {item_in.product_id} not found or insufficient quantity.")

        # Deduct quantity from inventory
        product.quantity -= item_in.quantity
        db.add(product) # Mark product for update

        # Calculate price for this item based on selling price at time of purchase
        item_total = item_in.quantity * product.selling_price
        total_amount += item_total

        db_order_item = models.OrderItem(
            product_id=item_in.product_id,
            quantity=item_in.quantity,
            price_at_purchase=product.selling_price # Store the price at time of purchase
        )
        db_order_items.append(db_order_item)

    db_order = models.Order(
        buyer_id=buyer_id,
        total_amount=total_amount,
        shipping_address=order.shipping_address,
        items=db_order_items # Link order items to the order
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[models.Order]:
    """Retrieve a list of all orders with pagination."""
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Order]:
    """Retrieve a list of orders for a specific user with pagination."""
    return db.query(models.Order).filter(models.Order.buyer_id == user_id).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    """Retrieve a single order by its ID."""
    return db.query(models.Order).filter(models.Order.id == order_id).first()

