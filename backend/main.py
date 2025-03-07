import uvicorn
import requests
from fastapi import FastAPI, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ----------------------
# CONFIG
# ----------------------
DATABASE_URL = "sqlite:///./scraped_data.db"
# Where is our Auth Microservice located?
AUTH_SERVICE_URL = "http://127.0.0.1:8001/auth/validate"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ----------------------
# SQLAlchemy Model
# ----------------------
class ScrapedItem(Base):
    __tablename__ = "scraped_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    filename = Column(String, index=True, nullable=True)
    content = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)

# ----------------------
# Pydantic Schemas
# ----------------------
class ScrapedItemBase(BaseModel):
    filename: Optional[str] = None
    content: str

class ScrapedItemCreate(ScrapedItemBase):
    pass

class ScrapedItemRead(ScrapedItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# This schema will represent the user info
class UserRead(BaseModel):
    id: int
    email: str

# ----------------------
# FASTAPI INIT & DEPENDENCIES
# ----------------------
app = FastAPI(title="Scraped Data Microservice")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request) -> UserRead:
    """
    Reads 'Authorization' header, calls Auth Microservice to validate token.
    Returns a `UserRead` object if valid, or raises HTTPException(401).
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )

    try:
        # Make a request to the Auth Microservice for validation
        response = requests.post(
            AUTH_SERVICE_URL,
            headers={"Authorization": auth_header},
            timeout=5
        )
        if response.status_code == 200:
            user_data = response.json()
            return UserRead(**user_data)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to contact Auth Microservice"
        )

# ----------------------
# Routes / Endpoints
# ----------------------
@app.get("/")
def root():
    return {"message": "Scraped Data Microservice Running!"}

@app.post("/scraped_data", response_model=ScrapedItemRead, tags=["scraped_data"])
def create_scraped_data(
    item: ScrapedItemCreate,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    """
    Create a new scraped data entry for the authenticated user.
    """
    db_item = ScrapedItem(
        user_id=current_user.id,
        filename=item.filename,
        content=item.content
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/scraped_data", response_model=List[ScrapedItemRead], tags=["scraped_data"])
def get_scraped_data(
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    """
    Get all scraped data for the authenticated user.
    """
    items = db.query(ScrapedItem).filter(ScrapedItem.user_id == current_user.id).all()
    return items

@app.get("/scraped_data/{item_id}", response_model=ScrapedItemRead, tags=["scraped_data"])
def get_scraped_data_by_id(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    """
    Get a single scraped data record by ID if it belongs to the current user.
    """
    db_item = db.query(ScrapedItem).filter(ScrapedItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized for this item")
    return db_item

# -----------------------------------------------------------------------------
#                               MAIN ENTRY POINT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("scraped_data_microservice:app", host="127.0.0.1", port=8002, reload=True)
