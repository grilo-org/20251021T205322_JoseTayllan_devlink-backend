from fastapi import APIRouter, Depends, HTTPException
from app import schemas, models
from app.core.security import get_current_user
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.core.security import get_current_user
import shutil
import os


router = APIRouter(prefix="/users", tags=["users"])

UPLOAD_DIR = "uploads"

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/update", response_model=schemas.UserResponse)
def update_user(
    db: Session = Depends(database.get_db),
    user=Depends(get_current_user),
    name: str = Form(None),
    role: str = Form(None),
    bio: str = Form(None),
    file: UploadFile | None = File(None)
):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if name:
        db_user.name = name
    if role:
        db_user.role = role
    if bio:
        db_user.bio = bio

    # 🔹 upload da foto de perfil
    if file:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, f"user_{user.id}.jpg")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        db_user.photo_url = f"http://127.0.0.1:8000/{file_path}"

    db.commit()
    db.refresh(db_user)
    return db_user