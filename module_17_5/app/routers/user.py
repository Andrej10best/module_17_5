from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/{user_id}')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id)).all()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    # Выполняется проверка на наличие добавленного пользователя
    existing_users = db.scalars(select(User).where(User.username == create_user.username, User.firstname ==
                                                   create_user.firstname, User.lastname ==
                                                   create_user.lastname)).first()
    if existing_users:
        return {
            'status_code': status.HTTP_400_BAD_REQUEST,
            'transaction': 'A user with that name already exists'
        }
    else:
        db.execute(insert(User).values(username=create_user.username,
                                       firstname=create_user.firstname,
                                       lastname=create_user.lastname,
                                       age=create_user.age,
                                       slug=create_user.username))
        db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    users = db.scalar(select(User).where(User.id == user_id))
    if users:
        db.execute(update(User).where(User.id == user_id).values(
            firstname=update_user.firstname,
            lastname=update_user.lastname,
            age=update_user.age))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalar(select(User).where(User.id == user_id))
    if users:
        db.execute(delete(User).where(User.id == user_id))
        db.execute(delete(Task).where(Task.user_id == user_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'The user has been deleted'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )


@router.get('/user_id/tasks')
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalar(select(User).where(User.id == user_id))
    if users:
        tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
        if tasks:
            return tasks
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task was not found'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
