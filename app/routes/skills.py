from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas,  database
from app.core.security import get_current_user

router = APIRouter(prefix="/skills", tags=["skills"])

#Create a new skill
@router.post("/", response_model=schemas.SkillResponse)
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(database.get_db), user= Depends(get_current_user)):
    new_skill = models.Skill(name=skill.name,level=skill.level, user_id=user.id)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill

# List Skills of the logged-in user
@router.get("/", response_model=list[schemas.SkillResponse])
def list_skills(db: Session = Depends(database.get_db), user= Depends(get_current_user)):
    skills = db.query(models.Skill).filter(models.Skill.user_id == user.id).all()
    return skills


# Delete a skill by ID
@router.delete("/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(database.get_db), user= Depends(get_current_user)):
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id, models.Skill.user_id == user.id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return {"detail": "Skill deleted successfully"}