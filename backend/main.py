from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import func
from starlette.concurrency import run_in_threadpool
from database import engine, SessionLocal
from models import Base, User, Receipt, ReceiptItem
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import JWTError, jwt
import pytesseract
from PIL import Image
from scripts import get_product
import re
import os
from io import BytesIO
from datetime import datetime, timedelta
app = FastAPI()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class CategoryStatsRequest(BaseModel):
    receipt_ids: list[int] | None = None


class CategoryItemsRequest(BaseModel):
    category: str
    receipt_ids: list[int] | None = None

# Dependency to get the database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Function to verify the password, which checks if the stored password is hashed and verifies it accordingly
def verify_password(plain_password: str, stored_password: str) -> bool:
    if pwd_context.identify(stored_password):
        return pwd_context.verify(plain_password, stored_password)
    return plain_password == stored_password

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if user_id is None:
            raise credentials_exception
        if token_type != "access":
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

Base.metadata.create_all(bind=engine)
@app.get("/")
async def home():
    return {"message": "Hello World"}
@app.get("/test")
async def test():
    return {"status": "working"}


@app.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }


@app.post("/register")
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    if len(data.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be 72 bytes or fewer",
        )
    print("password type:", type(data.password))
    print("password length:", len(data.password))
    print("password byte length:", len(data.password.encode("utf-8")))

    hashed_password = pwd_context.hash(data.password)
    user = User(username=data.username, email=data.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "registered", "user_id": user.id}


@app.post("/refresh")
async def refresh_tokens(data: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.get("/receipts")
async def list_receipts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    receipts = (
        db.query(Receipt)
        .filter(Receipt.user_id == current_user.id)
        .order_by(Receipt.created_at.desc())
        .all()
    )
    response = []
    for index, receipt in enumerate(receipts, start=1):
        response.append(
            {
                "id": receipt.id,
                "created_at": receipt.created_at.isoformat(),
                "number": index,
            }
        )
    return response


@app.delete("/receipts/{receipt_id}")
async def delete_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    receipt = (
        db.query(Receipt)
        .filter(Receipt.id == receipt_id, Receipt.user_id == current_user.id)
        .first()
    )
    if not receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")

    db.query(ReceiptItem).filter(ReceiptItem.receipt_id == receipt.id).delete()
    db.delete(receipt)
    db.commit()
    return {"message": "deleted"}


@app.post("/stats/categories")
async def category_stats(
    data: CategoryStatsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(ReceiptItem.category, func.sum(ReceiptItem.price))
        .join(Receipt, ReceiptItem.receipt_id == Receipt.id)
        .filter(Receipt.user_id == current_user.id)
    )

    if data.receipt_ids:
        query = query.filter(Receipt.id.in_(data.receipt_ids))

    rows = query.group_by(ReceiptItem.category).all()
    return [
        {"category": category or "Uncategorized", "total": float(total or 0)}
        for category, total in rows
    ]


@app.post("/stats/category-items")
async def category_items(
    data: CategoryItemsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(ReceiptItem)
        .join(Receipt, ReceiptItem.receipt_id == Receipt.id)
        .filter(Receipt.user_id == current_user.id)
    )

    if data.receipt_ids:
        query = query.filter(Receipt.id.in_(data.receipt_ids))

    if data.category == "Uncategorized":
        query = query.filter(ReceiptItem.category.is_(None))
    else:
        query = query.filter(ReceiptItem.category == data.category)

    items = query.order_by(ReceiptItem.name.asc()).all()
    return [
        {
            "name": item.name or "N/A",
            "price": float(item.price or 0),
            "description": item.description or "N/A",
        }
        for item in items
    ]
@app.post("/upload")
async def upload_image(file: UploadFile = File(...),
                       
                       db : Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    if file.content_type not in {"image/jpeg", "image/png", "image/webp", "image/tiff", "image/bmp"}:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty upload")
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")
    image = Image.open(BytesIO(contents))
    image.load()
    text = pytesseract.image_to_string(image)
    regular = re.findall(r'(\d{12}).*?\$(\d+\.\d{2})', text)
    bulk = re.findall(
    r'(0{6}\d{6})\s*\n\s*\d+(?:\.\d+)?\s*kg\s*@\s*\$\d+\.\d{2}\s*/kg\s*\$(\d+\.\d{2})',
    text)    
    if bulk:
        print("Price ="+ bulk[0][0] +"code = " + bulk[0][1])
    # Combine and sort by their position in the text
    all_items = []
    for code, price in regular + bulk:
        pos = text.find(code)
        all_items.append((pos, code, price))

    all_items.sort(key=lambda x: x[0])

    codes  = [code  for _, code,  _     in all_items]
    prices = [price for _, _,  price in all_items]

    
    
    receipt = Receipt(
        user_id=current_user.id,
        ocr_text=text
    )
    db.add(receipt)

    db.commit()

    db.refresh(receipt)    
    for code, price in zip(codes, prices):
        name, category, brand, description = get_product(code)        
        receipt_item = ReceiptItem(
            receipt_id=receipt.id,
            barcode=code,
            category=category,
            brand=brand,
            description=description,
            price = float(price.replace("$", "")),
            name = name
        )
        db.add(receipt_item)
        db.commit()
        db.refresh(receipt_item)


    db.commit()


    