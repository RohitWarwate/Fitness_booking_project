# Fitness Studio Booking API

Simple booking API built with FastAPI and SQLite for a fictional fitness studio.

## Features
- Signup / Login (JWT)
- Create, list fitness classes
- Book slots in classes (prevents overbooking)
- View user bookings
- Class times stored in **IST (Asia/Kolkata)**

## Requirements
- Python 3.10+
- Install with `pip install -r requirements.txt`

## Run locally
1. Create virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate     # Linux/Mac
   venv\Scripts\activate        # Windows
   pip install -r requirements.txt
