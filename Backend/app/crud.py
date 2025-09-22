# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from . import models, schemas


# ================= USERS ================= #
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = generate_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()  # type: ignore

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first() # type: ignore

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# ================= CLASSES ================= #
def create_class(db: Session, class_: schemas.ClassBase):
    db_class = models.Class(**class_.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def get_class(db: Session, class_id: int):
    return db.query(models.Class).filter(models.Class.id == class_id).first() # type: ignore

def get_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Class).offset(skip).limit(limit).all()

def get_average_rating_for_class(db: Session, class_id: int):
    avg = db.query(func.avg(models.Comment.rating)).filter(
        models.Comment.class_id == class_id, # type: ignore
        models.Comment.rating.isnot(None)             # type: ignore
    ).scalar()
    return avg or 0


# ================= ENROLLMENTS ================= #
def enroll_user(db: Session, user_id: int, class_id: int):
    db_enrollment = models.Enrollment(
        user_id=user_id,
        class_id=class_id
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def get_enrollments_by_user(db: Session, user_id: int):
    return db.query(models.Enrollment).filter(models.Enrollment.user_id == user_id).all() # type: ignore

def get_enrollments_by_class(db: Session, class_id: int):
    return db.query(models.Enrollment).filter(models.Enrollment.class_id == class_id).all() # type: ignore


# ================= COMMENTS ================= #
def add_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(
        user_id=comment.user_id,
        class_id=comment.class_id,
        content=comment.content,
        rating=comment.rating
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_class(db: Session, class_id: int):
    return db.query(models.Comment).filter(models.Comment.class_id == class_id).all() # type: ignore

def get_comment_by_user_for_class(db: Session, user_id: int, class_id: int):
    return db.query(models.Comment).filter(
        models.Comment.user_id == user_id,  # type: ignore
        models.Comment.class_id == class_id          # type: ignore
    ).first()


# ================= ACHIEVEMENTS ================= #
def add_achievement(db: Session, user_id: int, type: str, points: int):
    db_achievement = models.Achievement(
        user_id=user_id,
        type=type,
        points=points
    )
    db.add(db_achievement)

    # actualizar puntos del usuario
    user = db.query(models.User).filter(models.User.id == user_id).first() # type: ignore
    if user:
        user.points += points

    db.commit()
    db.refresh(db_achievement)
    return db_achievement

def get_achievements_by_user(db: Session, user_id: int):
    return db.query(models.Achievement).filter(models.Achievement.user_id == user_id).all() # type: ignore
