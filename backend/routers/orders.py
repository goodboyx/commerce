from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.connection import get_db
from services.order_service import OrderService
from schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    OrderStatusUpdate,
    PaymentStatusUpdate
)
from models.order import OrderStatus, PaymentStatus
from typing import Optional

router = APIRouter(prefix="/orders", tags=["orders"])
order_service = OrderService()

@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    """장바구니에서 주문 생성"""
    try:
        order = order_service.create_order_from_cart(
            db=db,
            cart_id=order_data.cart_id,
            email=order_data.email,
            shipping_address=order_data.shipping_address,
            billing_address=order_data.billing_address,
            notes=order_data.notes
        )
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, db: Session = Depends(get_db)):
    """주문 조회"""
    try:
        order = order_service.get_order(db=db, order_id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/number/{order_number}", response_model=OrderResponse)
async def get_order_by_number(order_number: str, db: Session = Depends(get_db)):
    """주문 번호로 주문 조회"""
    try:
        order = order_service.get_order_by_number(db=db, order_number=order_number)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=OrderListResponse)
async def get_user_orders(
    user_id: str,
    page: int = Query(1, ge=1, description="페이지 번호"),
    per_page: int = Query(20, ge=1, le=100, description="페이지당 항목 수"),
    db: Session = Depends(get_db)
):
    """사용자 주문 목록 조회"""
    try:
        result = order_service.get_user_orders(
            db=db,
            user_id=user_id,
            page=page,
            per_page=per_page
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    """주문 상태 업데이트"""
    try:
        order = order_service.update_order_status(
            db=db,
            order_id=order_id,
            status=status_update.status
        )
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{order_id}/payment", response_model=OrderResponse)
async def update_payment_status(
    order_id: str,
    payment_update: PaymentStatusUpdate,
    db: Session = Depends(get_db)
):
    """결제 상태 업데이트"""
    try:
        order = order_service.update_payment_status(
            db=db,
            order_id=order_id,
            payment_status=payment_update.payment_status,
            payment_id=payment_update.payment_id,
            payment_method=payment_update.payment_method
        )
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: str, db: Session = Depends(get_db)):
    """주문 취소"""
    try:
        order = order_service.cancel_order(db=db, order_id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
