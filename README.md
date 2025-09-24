# 한국어 커머스 플랫폼

Vercel Commerce를 기반으로 한 한국어 버전 전자상거래 플랫폼입니다. Next.js 프론트엔드와 FastAPI 백엔드로 구성된 풀스택 애플리케이션입니다.

## 🏗️ 프로젝트 구조

```
commerce/
├── app/                    # Next.js 프론트엔드 (한국어 버전)
├── backend/               # FastAPI 백엔드 서버
├── sql/                   # 데이터베이스 스키마 및 샘플 데이터
└── README.md             # 프로젝트 문서
```

## 📋 기술 스택

### 프론트엔드 (app/)
- **Framework**: Next.js 15.3.0 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4.0
- **UI Components**: Headless UI, Heroicons
- **State Management**: React Server Components, Server Actions
- **Package Manager**: pnpm

### 백엔드 (backend/)
- **Framework**: FastAPI 0.104.1
- **Language**: Python 3.x
- **Database**: MariaDB/MySQL with SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Payment**: Stripe integration
- **Caching**: Redis
- **File Upload**: Pillow for image processing

### 데이터베이스 (sql/)
- **Database**: MariaDB/MySQL
- **ORM**: SQLAlchemy
- **Migration**: Alembic
- **Character Set**: utf8mb4

## 🚀 시작하기

### 사전 요구사항

- Node.js 18+ 및 pnpm
- Python 3.8+
- MariaDB/MySQL 서버
- Redis 서버 (선택사항)

### 1. 데이터베이스 설정

```bash
# MariaDB/MySQL에 접속하여 데이터베이스 초기화
mysql -u root -p < sql/init_database.sql

# 샘플 데이터 삽입
mysql -u root -p commerce_db < sql/sample_data.sql
```

### 2. 백엔드 설정 및 실행

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정 (.env 파일 생성)
cp .env.example .env

# .env 파일에서 실제 데이터베이스 정보로 수정
# DATABASE_URL=mysql+pymysql://실제사용자명:실제비밀번호@실제호스트:3306/실제데이터베이스명

# 서버 실행
python main.py
```

백엔드 서버는 `http://localhost:8013`에서 실행됩니다.

### 3. 프론트엔드 설정 및 실행

```bash
cd app

# 의존성 설치
pnpm install

# 환경변수 설정
cp .env.example .env.local
# FASTAPI_BASE_URL=http://localhost:8013 설정

# 개발 서버 실행
pnpm dev
```

프론트엔드는 `http://localhost:3000`에서 실행됩니다.

## 📁 주요 디렉토리 구조

### 프론트엔드 (app/)
```
app/
├── app/                   # Next.js App Router 페이지
│   ├── page.tsx          # 홈페이지
│   ├── product/          # 상품 상세 페이지
│   ├── search/           # 검색 페이지
│   └── checkout/         # 결제 페이지
├── components/           # 재사용 가능한 컴포넌트
│   ├── cart/            # 장바구니 관련 컴포넌트
│   ├── layout/          # 레이아웃 컴포넌트
│   └── product/         # 상품 관련 컴포넌트
├── lib/                 # 유틸리티 및 API 클라이언트
│   ├── fastapi/         # FastAPI 백엔드 연결
│   └── shopify/         # Shopify API (원본 유지)
└── package.json
```

### 백엔드 (backend/)
```
backend/
├── main.py              # FastAPI 애플리케이션 진입점
├── core/                # 핵심 설정
│   └── config.py       # 환경 설정
├── models/              # SQLAlchemy 데이터베이스 모델
│   ├── product.py      # 상품 모델
│   ├── cart.py         # 장바구니 모델
│   ├── order.py        # 주문 모델
│   └── user.py         # 사용자 모델
├── routers/             # API 라우터
│   ├── products.py     # 상품 API
│   ├── cart.py         # 장바구니 API
│   ├── collections.py  # 컬렉션 API
│   └── orders.py       # 주문 API
├── schemas/             # Pydantic 스키마
├── services/            # 비즈니스 로직
└── requirements.txt
```

### 데이터베이스 (sql/)
```
sql/
├── init_database.sql        # 데이터베이스 및 테이블 생성
├── sample_data.sql         # 샘플 데이터
├── fixed_database.sql      # 수정된 데이터베이스 스키마
└── fixed_sample_data.sql   # 수정된 샘플 데이터
```

## 🔧 주요 기능

### 프론트엔드 기능
- 🛍️ 상품 카탈로그 및 검색
- 🛒 장바구니 관리
- 💳 결제 프로세스
- 📱 반응형 디자인
- 🌐 한국어 지원
- ⚡ Server-Side Rendering (SSR)

### 백엔드 기능
- 🔐 JWT 기반 인증
- 📦 상품 관리 API
- 🛒 장바구니 및 주문 처리
- 💾 파일 업로드
- 💳 Stripe 결제 연동
- 📊 API 문서 자동 생성 (FastAPI Docs)

### 데이터베이스 스키마
- 👥 사용자 관리
- 📦 상품 및 컬렉션
- 🛒 장바구니 및 주문
- 🏷️ 상품 옵션 및 변형

## 🔗 API 엔드포인트

백엔드 서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- **Swagger UI**: `http://localhost:8013/docs`
- **ReDoc**: `http://localhost:8013/redoc`

### 주요 API 엔드포인트
- `GET /api/v1/products/` - 상품 목록
- `GET /api/v1/products/{handle}` - 상품 상세
- `GET /api/v1/collections/` - 컬렉션 목록
- `POST /api/v1/cart/add` - 장바구니 추가
- `GET /health` - 서버 상태 확인

## 🛠️ 개발 가이드

### 환경 설정

#### 백엔드 환경변수 (.env)
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://실제사용자명:실제비밀번호@실제호스트:3306/실제데이터베이스명
REDIS_HOST=localhost
STRIPE_SECRET_KEY=your-stripe-secret-key
JWT_SECRET_KEY=jwt-secret-key
```

> ⚠️ **보안 주의사항**: `.env` 파일은 실제 데이터베이스 정보를 포함하므로 Git에 커밋하지 마세요. 이미 `.gitignore`에 포함되어 있습니다.

#### 프론트엔드 환경변수 (.env.local)
```env
FASTAPI_BASE_URL=http://localhost:8013
NEXT_PUBLIC_SITE_NAME=한국어 커머스
```

### 코드 스타일
- **프론트엔드**: Prettier + ESLint
- **백엔드**: Black + isort

### 테스트
```bash
# 백엔드 테스트
cd backend
pytest

# 프론트엔드 테스트
cd app
pnpm test
```

## 📈 성능 최적화

- **프론트엔드**: React Server Components, 이미지 최적화, 코드 분할
- **백엔드**: 데이터베이스 연결 풀링, Redis 캐싱, 비동기 처리
- **데이터베이스**: 인덱스 최적화, 쿼리 최적화

## 🔒 보안

- JWT 토큰 기반 인증
- CORS 설정
- SQL 인젝션 방지 (SQLAlchemy ORM)
- 파일 업로드 검증
- 환경변수를 통한 민감 정보 관리

## 🚀 배포

### 프론트엔드 (Vercel)
```bash
cd app
vercel --prod
```

### 백엔드 (Docker)
```bash
cd backend
docker build -t commerce-backend .
docker run -p 8013:8013 commerce-backend
```

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙏 감사의 말

- [Vercel Commerce](https://github.com/vercel/commerce) - 원본 프로젝트
- [FastAPI](https://fastapi.tiangolo.com/) - 백엔드 프레임워크
- [Next.js](https://nextjs.org/) - 프론트엔드 프레임워크

## 📞 문의

프로젝트에 대한 문의사항이나 버그 리포트는 GitHub Issues를 통해 제출해 주세요.
