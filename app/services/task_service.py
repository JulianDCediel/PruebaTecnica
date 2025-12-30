from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Task)
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_tasks_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Task)
        .filter(Task.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_task(db: Session, task_data: TaskCreate, owner_id: int):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        owner_id=owner_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def complete_task(db: Session, task: Task):
    task.completed = True
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, data: TaskUpdate):
    task.title = data.title
    task.description = data.description
    task.completed = data.completed

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()