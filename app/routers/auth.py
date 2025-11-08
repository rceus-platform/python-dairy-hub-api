from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import auth as schemas

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Query the admin table for the provided username and password
    query = text("""
        SELECT username FROM public.admin 
        WHERE username = :username AND password = :password
    """)
    result = db.execute(
        query,
        {"username": credentials.username, "password": credentials.password},
    )

    admin = result.first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {"status": "success", "message": "Login successful"}
