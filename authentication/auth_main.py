import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from fastapi.middleware.cors import CORSMiddleware
# -----------------------------------------------------------------------------
#                           CONFIG & DATABASE SETUP
# -----------------------------------------------------------------------------
DATABASE_URL = "sqlite:///./user_auth.db"
SECRET_KEY = "CHANGE_THIS_TO_SOMETHING_SECURE"  # Load from env in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# -----------------------------------------------------------------------------
#                           PASSWORD HASHING
# -----------------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -----------------------------------------------------------------------------
#                           DATABASE MODELS
# -----------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# -----------------------------------------------------------------------------
#                           Pydantic Schemas
# -----------------------------------------------------------------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# -----------------------------------------------------------------------------
#                        TOKEN CREATION & VALIDATION
# -----------------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> int:
    """
    Decode the JWT, return the user_id if valid,
    or raise HTTPException if invalid/expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token missing 'sub'")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# -----------------------------------------------------------------------------
#                           FASTAPI INIT & DEPENDENCIES
# -----------------------------------------------------------------------------
app = FastAPI(title="Auth Microservice")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------------------------------------------------------
#                             AUTH ENDPOINTS
# -----------------------------------------------------------------------------
@app.post("/auth/signup", response_model=UserRead, tags=["auth"])
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.
    """
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/auth/login", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Log in with (username=email, password).
    Returns a JWT token if credentials are correct.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/auth/validate", response_model=UserRead, tags=["auth"])
def validate_token(request: Request, db: Session = Depends(get_db)):
    """
    Validate the token from the Authorization header.
    Return user data if valid; else raise 401.
    This endpoint is called by the 'scraped_data' microservice.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header"
        )
    token = auth_header[len("Bearer ") :]

    user_id = decode_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return UserRead(id=user.id, email=user.email)

@app.get("/", tags=["root"])
def root():
    return {"message": "Auth Microservice Running!"}

# -----------------------------------------------------------------------------
#                               MAIN ENTRY POINT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("auth_microservice:app", host="127.0.0.1", port=8001, reload=True)
