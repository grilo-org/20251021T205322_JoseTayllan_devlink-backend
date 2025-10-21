from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.core.security import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

# ✅ Criar novo projeto
@router.post("/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    new_project = models.Project(
        title=project.title,
        description=project.description,
        link=project.link,
        user_id=user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


# ✅ Listar todos os projetos do usuário logado
@router.get("/", response_model=list[schemas.ProjectResponse])
def get_projects(db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    projects = db.query(models.Project).filter(models.Project.user_id == user.id).all()
    return projects


# ✅ Deletar projeto específico
@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.user_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    db.delete(project)
    db.commit()
    return {"message": "Projeto removido com sucesso"}
