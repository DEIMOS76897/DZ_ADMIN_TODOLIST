from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from auth import get_current_admin_user
from database import get_db
from models import User, Note
from schemas import UserResponce, NoteResponce

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=list[UserResponce])
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)):
    return db.query(User).all()

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такого юзера нет"
        )
    db.delete(user)
    db.commit()
    return {"message": "Пользователь удалён"}

@router.get("/notes", response_model=list[NoteResponce])
def get_all_notes(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)):
    return db.query(Note).all()