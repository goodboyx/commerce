from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import time
import logging
import os
from fastapi.responses import RedirectResponse

from core.config import settings
from database.connection import engine, test_db_connection
from models import *  # 모든 모델 import
from routers import products, cart, collections, orders


# 로깅 설정
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

# 업로드 디렉토리 생성
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# FastAPI 앱 생성
app = FastAPI(
    title="Commerce API",
    description="FastAPI + MariaDB 기반 커머스 API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS if settings.ALLOWED_HOSTS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 시간 측정 미들웨어
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,    
    return response



# 전역 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc) if settings.DEBUG else "Internal server error"}
    )

@app.get("/", tags=["/"])
async def root(summary="/ 접속시 docs로 이동"):
    return RedirectResponse(url="/docs")

# 정적 파일 서빙
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 라우터 등록
app.include_router(products.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(collections.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")

# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    """서버 상태 확인"""
    db_status = test_db_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "timestamp": time.time(),
        "database": "connected" if db_status else "disconnected",
        "version": "1.0.0"
    }

# 루트 엔드포인트
@app.get("/")
async def root():
    """API 정보"""
    return {
        "message": "Commerce API",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG else "Documentation not available in production",
        "health": "/health"
    }

# 데이터베이스 테이블 생성
@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    try:        
        # 데이터베이스 연결 테스트
        if test_db_connection():
            logger.info("Database connection successful")
        else:
            logger.error("Database connection failed")
            
    except Exception as e:
        logger.error(f"Startup error: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info("Application shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8013,
        reload=settings.DEBUG,
        log_level="info"
    )
