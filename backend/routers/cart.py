from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from services.cart_service import CartService
from schemas.cart import (
    CartCreate,
    CartResponse,
    AddToCartRequest,
    UpdateCartRequest,
    RemoveFromCartRequest
)

router = APIRouter(prefix="/cart", tags=["cart"])
cart_service = CartService()

@router.post("/", response_model=CartResponse, status_code=201)
async def create_cart(
    cart_data: CartCreate,
    db: Session = Depends(get_db)
):
    """새 장바구니 생성"""
    try:
        cart = cart_service.create_cart(db=db, cart_data=cart_data)
        return cart
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{cart_id}", response_model=CartResponse)
async def get_cart(cart_id: str, db: Session = Depends(get_db)):
    """장바구니 조회"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Getting cart with ID: {cart_id}")
        cart = cart_service.get_cart(db=db, cart_id=cart_id)
        logger.info(f"Cart service returned: {cart}")
        
        if not cart:
            logger.warning(f"Cart not found: {cart_id}")
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_cart endpoint: {e}")
        logger.error(f"Exception type: {type(e)}")
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/{cart_id}/items", response_model=CartResponse)
async def add_to_cart(
    cart_id: str,
    request: AddToCartRequest,
    db: Session = Depends(get_db)
):
    """장바구니에 상품 추가"""
    try:
        cart = cart_service.add_items_to_cart(
            db=db, 
            cart_id=cart_id, 
            items=request.items
        )
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{cart_id}/items", response_model=CartResponse)
async def update_cart_items(
    cart_id: str,
    request: UpdateCartRequest,
    db: Session = Depends(get_db)
):
    """장바구니 상품 수량 업데이트"""
    try:
        cart = cart_service.update_cart_items(
            db=db, 
            cart_id=cart_id, 
            items=request.items
        )
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{cart_id}/items")
async def remove_from_cart(
    cart_id: str,
    request: RemoveFromCartRequest,
    db: Session = Depends(get_db)
):
    """장바구니에서 상품 제거"""
    try:
        success = cart_service.remove_items_from_cart(
            db=db, 
            cart_id=cart_id, 
            item_ids=request.item_ids
        )
        if not success:
            raise HTTPException(status_code=404, detail="Cart or items not found")
        return {"message": f"{len(request.item_ids)} items removed successfully"}
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{cart_id}/clear")
async def clear_cart(cart_id: str, db: Session = Depends(get_db)):
    """장바구니 비우기"""
    try:
        success = cart_service.clear_cart(db=db, cart_id=cart_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cart not found")
        return {"message": "Cart cleared successfully"}
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{cart_id}")
async def delete_cart(cart_id: str, db: Session = Depends(get_db)):
    """장바구니 삭제"""
    try:
        success = cart_service.delete_cart(db=db, cart_id=cart_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cart not found")
        return {"message": "Cart deleted successfully"}
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}", response_model=CartResponse)
async def get_cart_by_session(session_id: str, db: Session = Depends(get_db)):
    """세션 ID로 장바구니 조회"""
    try:
        cart = cart_service.get_cart_by_session(db=db, session_id=session_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
