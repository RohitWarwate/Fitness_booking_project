# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas, auth, crud
from app.database import engine, Base
from app.deps import get_db
from datetime import timedelta
from zoneinfo import ZoneInfo
from typing import List, Optional
from dateutil import parser

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Studio Booking API")
IST = ZoneInfo("Asia/Kolkata")

@app.post("/signup", response_model=schemas.Token)
def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in)
    access_token = auth.create_access_token({"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = auth.create_access_token({"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/classes", response_model=schemas.ClassOut)
def create_class(c: schemas.ClassCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    created = crud.create_class(db, c)
    return {
        "id": created.id,
        "name": created.name,
        "dateTime": created.date_time,
        "instructor": created.instructor,
        "availableSlots": created.available_slots
    }

@app.get("/classes", response_model=List[schemas.ClassOut])
def get_classes(tz: Optional[str] = None, db: Session = Depends(get_db)):
    classes = crud.list_upcoming_classes(db)
    out = []
    for c in classes:
        dt = c.date_time
        if tz:
            try:
                target = ZoneInfo(tz)
                dt = dt.astimezone(target)
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid timezone")
        out.append({
            "id": c.id,
            "name": c.name,
            "dateTime": dt,
            "instructor": c.instructor,
            "availableSlots": c.available_slots
        })
    return out

@app.post("/book", response_model=schemas.BookingOut)
def book_slot(req: schemas.BookRequest, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    booking, err = crud.create_booking(db, current_user, req)
    if err == "class_not_found":
        raise HTTPException(status_code=404, detail="Class not found")
    if err == "no_slots":
        raise HTTPException(status_code=400, detail="No available slots")
    return booking

@app.get("/bookings", response_model=List[schemas.BookingOut])
def my_bookings(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    bookings = crud.get_bookings_for_user(db, current_user)
    return bookings
