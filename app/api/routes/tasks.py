from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import (
    create_task,
    get_task_by_id,
    list_tasks_by_user,
    complete_task, update_task, delete_task, list_tasks,
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])



@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task(db, task, owner_id=current_user.id)


@router.get("/", response_model=list[TaskRead])
def get_my_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_tasks_by_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

@router.get("/all", response_model=list[TaskRead])
def get_all_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
):
    return list_tasks(db, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=TaskRead)
def get_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(db, task_id)

    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}", response_model=TaskRead)
def update(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(db, task_id)

    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    return update_task(db, task, task_data)


@router.patch("/{task_id}/complete", response_model=TaskRead)
def complete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(db, task_id)

    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    return complete_task(db, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(db, task_id)

    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    delete_task(db, task)