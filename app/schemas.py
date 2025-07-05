# app/schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# --- User Schemas ---

class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    """Schema for creating a new user (includes password)."""
    password: str = Field(..., min_length=8)
    is_admin: Optional[bool] = False # Allow setting admin status during creation

class UserUpdate(UserBase):
    """Schema for updating an existing user."""
    # Password is not included here for update, as it would be a separate endpoint
    # or a specific password change endpoint.
    pass

class UserInDB(UserBase):
    """Schema for user data as stored in the database (includes ID and hashed password)."""
    id: int
    hashed_password: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True # Changed from orm_mode = True for Pydantic v2

class UserResponse(UserBase):
    """Schema for user data returned in API responses (excludes hashed password)."""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True # Changed from orm_mode = True for Pydantic v2

class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema for data contained within a JWT token."""
    email: Optional[str] = None
    # You might add user ID or roles here if needed for authorization checks

# --- Product Schemas ---

class ProductBase(BaseModel):
    """Base schema for product data."""
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0) # Inventory quantity
    buying_price: float = Field(..., gt=0) # Cost to acquire
    selling_price: float = Field(..., gt=0) # Price for sale

class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    pass

class ProductUpdate(ProductBase):
    """Schema for updating an existing product."""
    # All fields are optional for update, allowing partial updates
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    buying_price: Optional[float] = None
    selling_price: Optional[float] = None

class ProductResponse(ProductBase):
    """Schema for product data returned in API responses."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True # Changed from orm_mode = True for Pydantic v2

# --- Order Schemas ---

class OrderItemBase(BaseModel):
    """Base schema for an item within an order."""
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderItemCreate(OrderItemBase):
    """Schema for creating a new order item."""
    pass

class OrderItemResponse(OrderItemBase):
    """Schema for an order item returned in API responses."""
    id: int
    order_id: int
    price_at_purchase: float # The price of the product when it was bought
    created_at: datetime

    class Config:
        from_attributes = True # Changed from orm_mode = True for Pydantic v2

class OrderBase(BaseModel):
    """Base schema for order data."""
    shipping_address: str

class OrderCreate(OrderBase):
    """Schema for creating a new order (includes items)."""
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    """Schema for order data returned in API responses."""
    id: int
    buyer_id: int
    total_amount: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemResponse] = [] # List of items in the order

    class Config:
        from_attributes = True # Changed from orm_mode = True for Pydantic v2

