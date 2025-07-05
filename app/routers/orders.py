# app/routers/orders.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED
)
def create_order_endpoint(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Create a new order for the current authenticated user.
    Deducts product quantities from inventory.
    """
    try:
        db_order = crud.create_user_order(db=db, order=order, buyer_id=current_user.id)
        # Eager load items for the response
        db_order_with_items = (
            db.query(models.Order)
            .options(joinedload(models.Order.items))
            .filter(models.Order.id == db_order.id)
            .first()
        )
        return db_order_with_items
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me", response_model=List[schemas.OrderResponse])
def read_my_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Retrieve a list of orders made by the current authenticated user.
    """
    orders = (
        db.query(models.Order)
        .options(joinedload(models.Order.items))
        .filter(models.Order.buyer_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return orders


@router.get("/{order_id}", response_model=schemas.OrderResponse)
def read_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Retrieve a specific order by ID.
    Only accessible by the buyer of the order or an admin.
    """
    db_order = (
        db.query(models.Order)
        .options(joinedload(models.Order.items))
        .filter(models.Order.id == order_id)
        .first()
    )
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    if db_order.buyer_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order",
        )
    return db_order


@router.get("/", response_model=List[schemas.OrderResponse])
def read_all_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        get_current_admin_user
    ),  # Only admins can view all orders
):
    """
    Retrieve a list of all orders in the system. Requires admin privileges.
    """
    orders = (
        db.query(models.Order)
        .options(joinedload(models.Order.items))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return orders
