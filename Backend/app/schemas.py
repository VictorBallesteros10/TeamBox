from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -------------------
# USER
# -------------------
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    avatar_url: Optional[str]
    role: str
    points: int
    created_at: datetime

    class Config:
        orm_mode = True


# -------------------
# CLASS
# -------------------
class ClassBase(BaseModel):
    title: str
    description: str
    date_time: datetime
    max_students: int

class Class(ClassBase):
    id: int
    video_url: Optional[str]
    photo_url: Optional[str]

    class Config:
        orm_mode = True


# -------------------
# COMMENT
# -------------------
class CommentBase(BaseModel):
    user_id: int
    class_id: int
    content: Optional[str] = None  # comentario opcional
    rating: Optional[int] = None   # rating opcional

class CommentCreate(BaseModel):
    user_id: int
    class_id: int
    content: Optional[str] = None
    rating: Optional[int] = None

# --------------------------
# Para devolver un comentario
# --------------------------

class Comment(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # para leer de SQLAlchemy


# -------------------
# ENROLLMENT
# -------------------
class EnrollmentBase(BaseModel):
    user_id: int
    class_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
    enrolled_at: datetime

    class Config:
        orm_mode = True


# -------------------
# ACHIEVEMENT
# -------------------
class AchievementBase(BaseModel):
    title: str
    description: Optional[str] = None

class AchievementCreate(AchievementBase):
    pass

class Achievement(AchievementBase):
    id: int
    user_id: int
    awarded_at: datetime

    class Config:
        orm_mode = True
