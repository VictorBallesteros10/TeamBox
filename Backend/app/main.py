# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TeamBox API")

# Permitir acceso desde tu frontend (React/Expo)
origins = [
    "http://localhost:19006",  # Expo Web
    "http://localhost:3000",   # React web
    "*",                       # Para pruebas rápidas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# USERS
# -------------------------
@app.get("/users", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# main.py
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)  # <- ya no pasamos password_hash


# -------------------------
# CLASSES
# -------------------------
@app.get("/classes/{class_id}/comments", response_model=list[schemas.Comment])
def read_comments_for_class(class_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_by_class(db, class_id)


@app.post("/classes", response_model=schemas.Class)
def create_class(class_: schemas.ClassBase, db: Session = Depends(get_db)):
    return crud.create_class(db=db, class_=class_)

@app.get("/classes", response_model=list[schemas.Class])
def read_classes(db: Session = Depends(get_db)):
    return crud.get_classes(db)

# -------------------------
# ENROLLMENTS
# -------------------------
@app.get("/enrollments")
def read_enrollments(db: Session = Depends(get_db)):
    return crud.get_enrollments(db)

@app.post("/enrollments")
def create_enrollment(user_id: int, class_id: int, db: Session = Depends(get_db)):
    return crud.create_enrollment(db=db, user_id=user_id, class_id=class_id)


# -------------------------
# COMMENTS & RATINGS
# -------------------------
@app.get("/comments")
def read_comments(db: Session = Depends(get_db)):
    return crud.get_comments_by_class(db)

@app.post("/comments", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.add_comment(db=db, comment=comment)

@app.get("/classes/{class_id}/my_comment/{user_id}", response_model=schemas.Comment)
def read_my_comment(class_id: int, user_id: int, db: Session = Depends(get_db)):
    comment = crud.get_comment_by_user_for_class(db, user_id, class_id)
    if not comment:
        return {"content": None, "rating": None, "user_id": user_id, "class_id": class_id}
    return comment

@app.get("/classes/{class_id}/average_rating")
def read_average_rating(class_id: int, db: Session = Depends(get_db)):
    return {"class_id": class_id, "average_rating": crud.get_average_rating_for_class(db, class_id)}

# -------------------------
# ACHIEVEMENTS
# -------------------------
@app.get("/achievements")
def read_achievements(db: Session = Depends(get_db)):
    return crud.get_achievements(db)

@app.post("/achievements")
def create_achievement(achievement: schemas.Achievement, db: Session = Depends(get_db)):
    return crud.create_achievement(db=db, achievement=achievement)
