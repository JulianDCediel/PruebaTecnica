from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate


def get_task_by_id(db: Session, task_id: int):
    """
    Obtiene una tarea por su ID.
    Retorna None si no existe.
    """
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(db: Session):
    """
    Retorna todas las tareas.
    """
    return db.query(Task).all()


def list_tasks_by_user(db: Session, user_id: int):
    """
    Retorna todas las tareas asociadas a un usuario.
    """
    return db.query(Task).filter(Task.owner_id == user_id).all()


def create_task(db: Session, task_data: TaskCreate, owner_id: int):
    """
    Crea una nueva tarea asociada a un usuario.
    """
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
    """
    Marca una tarea como completada.
    """
    task.completed = True
    db.commit()
    db.refresh(task)

    return task
