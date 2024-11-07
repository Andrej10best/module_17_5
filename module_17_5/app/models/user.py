from app.backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)

    tasks = relationship('Task', back_populates='user')

    # создал __init__, чтобы slug автоматически принимал значение  username
    def __init__(self, username, firstname=None, lastname=None, age=None):
        super().__init__()
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.slug = username

