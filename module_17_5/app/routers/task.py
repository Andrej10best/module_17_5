from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_task(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/{task_id}')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id)).all()
    if task:
        return task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], user_id: int, create_task: CreateTask):
    # Выполняется проверка на наличие пользователя
    existing_user = db.scalars(select(User).where(User.id == user_id)).first()
    if existing_user:
        db.execute(insert(Task).values(title=create_task.title,
                                       content=create_task.content,
                                       priority=create_task.priority,
                                       user_id=user_id,
                                       slug=create_task.title.lower()
                                       ))
        db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    tasks = db.scalar(select(Task).where(Task.id == task_id))
    if tasks:
        db.execute(update(Task).where(Task.id == task_id).values(
            title=update_task.title,
            content=update_task.content,
            priority=update_task.priority))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful!'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    tasks = db.scalar(select(Task).where(Task.id == task_id))
    if tasks:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'The task has been deleted'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
