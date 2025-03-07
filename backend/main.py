from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ----------------------
# Database configuration
# ----------------------
DATABASE_URL = "sqlite:///./scraped_data.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ----------------------
# SQLAlchemy Model
# ----------------------
class ScrapedItem(Base):
    __tablename__ = "scraped_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    filename = Column(String, index=True, nullable=True)
    content = Column(Text, nullable=False)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# ----------------------
# Pydantic Schemas
# ----------------------
class ScrapedItemBase(BaseModel):
    user_id: Optional[int] = None
    filename: Optional[str] = None
    content: str

class ScrapedItemCreate(ScrapedItemBase):
    """
    Schema for creating a new ScrapedItem.
    """
    pass

class ScrapedItemRead(ScrapedItemBase):
    id: int

    class Config:
        orm_mode = True

# ----------------------
# FastAPI Initialization
# ----------------------
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------
# Routes / Endpoints
# ----------------------

@app.get("/")
def root():
    return {"message": "Welcome to the Scraping Backend API!"}

@app.post("/scraped_data", response_model=ScrapedItemRead)
def create_scraped_data(item: ScrapedItemCreate, db: Session = Depends(get_db)):
    """
    Create a new scraped data entry.
    """
    db_item = ScrapedItem(
        user_id=item.user_id,
        filename=item.filename,
        content=item.content
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/scraped_data", response_model=List[ScrapedItemRead])
def get_scraped_data(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get all scraped data.  
    If `user_id` is provided, filter by that user_id.
    """
    query = db.query(ScrapedItem)
    if user_id is not None:
        query = query.filter(ScrapedItem.user_id == user_id)
    return query.all()

@app.get("/scraped_data/{item_id}", response_model=ScrapedItemRead)
def get_scraped_data_by_id(item_id: int, db: Session = Depends(get_db)):
    """
    Get a single scraped data record by ID.
    """
    db_item = db.query(ScrapedItem).filter(ScrapedItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
