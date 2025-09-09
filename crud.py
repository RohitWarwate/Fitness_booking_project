# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas, auth
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_class(db: Session, c: schemas.ClassCreate):
    # Ensure datetime is timezone-aware in IST
    dt = c.dateTime
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=IST)
    else:
        # convert to IST
        dt = dt.astimezone(IST)
    db_class = models.FitnessClass(
        name=c.name,
        date_time=dt,
        instructor=c.instructor,
        available_slots=c.availableSlots
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def list_upcoming_classes(db: Session):
    now_ist = datetime.now(IST)
    return db.query(models.FitnessClass).filter(models.FitnessClass.date_time >= now_ist).order_by(models.FitnessClass.date_time).all()

def get_class(db: Session, class_id: int):
    return db.query(models.FitnessClass).filter(models.FitnessClass.id == class_id).first()

def create_booking(db: Session, user: models.User, booking_req: schemas.BookRequest):
    cls = db.query(models.FitnessClass).filter(models.FitnessClass.id == booking_req.class_id).with_for_update(of=models.FitnessClass).first()
    if not cls:
        return None, "class_not_found"
    if cls.available_slots <= 0:
        return None, "no_slots"
    # Deduct slot and create booking in same transaction
    cls.available_slots -= 1
    booking = models.Booking(
        class_id=cls.id,
        user_id=user.id,
        client_name=booking_req.client_name,
        client_email=booking_req.client_email
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking, None

def get_bookings_for_user(db: Session, user: models.User):
    return db.query(models.Booking).filter(models.Booking.user_id == user.id).all()
