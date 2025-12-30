from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    list_users, delete_user, update_user,
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return create_user(db, user)


@router.get("/", response_model=list[UserRead])
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_users(db)

@router.get("/me", response_model=UserRead)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("/{user_id}", response_model=UserRead)
def get_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}", response_model=UserRead)
def update(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return update_user(db, user, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    delete_user(db, user)