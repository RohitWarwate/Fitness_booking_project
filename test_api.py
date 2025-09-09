# tests/test_api.py
# Simple integration checks (illustrative). For full tests use TestClient from fastapi.

from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_signup_and_login_and_flow():
    # signup
    resp = client.post("/signup", json={"name":"Rohit","email":"rohit@example.com","password":"password123"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create class
    class_payload = {
        "name":"Yoga Flow",
        "dateTime":"2025-10-01T10:00:00+05:30",
        "instructor":"John Doe",
        "availableSlots": 2
    }
    resp = client.post("/classes", json=class_payload, headers=headers)
    assert resp.status_code == 200
    class_id = resp.json()["id"]

    # book
    book_payload = {"class_id": class_id, "client_name": "Alice", "client_email": "alice@example.com"}
    resp = client.post("/book", json=book_payload, headers=headers)
    assert resp.status_code == 200

    # bookings list
    resp = client.get("/bookings", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
