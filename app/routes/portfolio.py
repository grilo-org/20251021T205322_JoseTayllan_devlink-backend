from fastapi import APIRouter, Depends, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader
from app import models, database
from app.core.security import get_current_user
import os

from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import io
import requests

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

@router.get("/html", response_class=HTMLResponse)
def get_portfolio_html(db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    # Coletar dados
    user_data = db.query(models.User).filter(models.User.id == user.id).first()
    skills = db.query(models.Skill).filter(models.Skill.user_id == user.id).all()
    projects = db.query(models.Project).filter(models.Project.user_id == user.id).all()

    # Carregar template
    template = env.get_template("portfolio.html")
    html = template.render(user=user_data, skills=skills, projects=projects)

    return HTMLResponse(content=html)

@router.get("/pdf")
def get_portfolio_pdf(db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    user_data = db.query(models.User).filter(models.User.id == user.id).first()
    skills = db.query(models.Skill).filter(models.Skill.user_id == user.id).all()
    projects = db.query(models.Project).filter(models.Project.user_id == user.id).all()

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    azul = colors.HexColor("#007bff")
    cinza_texto = colors.HexColor("#555")
    preto = colors.HexColor("#222")

    # 🔹 Cabeçalho com imagem
    pdf.setFillColor(azul)
    pdf.rect(0, height - 100, width, 100, fill=True, stroke=False)

    # Foto de perfil
    if user_data.photo_url:
        try:
            response = requests.get(user_data.photo_url, timeout=5)
            if response.status_code == 200:
                img = ImageReader(io.BytesIO(response.content))
                pdf.drawImage(img, 1.5 * cm, height - 90, 60, 60, mask='auto')
        except Exception:
            pass  # se a imagem falhar, ignora

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(7 * cm, height - 50, user_data.name)

    # Cargo (role)
    pdf.setFont("Helvetica-Oblique", 12)
    pdf.drawString(7 * cm, height - 70, user_data.role or "Profissional de Tecnologia")

    y = height - 130

    # 🔹 Bio
    if user_data.bio:
        pdf.setFont("Helvetica", 11)
        pdf.setFillColor(cinza_texto)
        pdf.drawString(2 * cm, y, "Resumo:")
        y -= 20
        text_object = pdf.beginText(2 * cm, y)
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor(preto)
        for line in user_data.bio.split("\n"):
            text_object.textLine(line)
        pdf.drawText(text_object)
        y = text_object.getY() - 15

    # 🔹 Skills
    pdf.setFillColor(azul)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(2 * cm, y, "Skills")
    pdf.line(2 * cm, y - 2, width - 2 * cm, y - 2)
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.setFillColor(preto)
    for skill in skills:
        pdf.drawString(2.5 * cm, y, f"• {skill.name} ({skill.level or 'Nível não informado'})")
        y -= 15
        if y < 100:
            pdf.showPage()
            y = height - 100

    y -= 10

    # 🔹 Projetos
    pdf.setFillColor(azul)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(2 * cm, y, "Projetos")
    pdf.line(2 * cm, y - 2, width - 2 * cm, y - 2)
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.setFillColor(preto)
    for project in projects:
        pdf.drawString(2.5 * cm, y, f"• {project.title}")
        y -= 13
        if project.description:
            pdf.setFont("Helvetica-Oblique", 10)
            pdf.setFillColor(cinza_texto)
            pdf.drawString(3 * cm, y, project.description[:90])
            y -= 13
        if project.link:
            pdf.setFillColor(azul)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(3 * cm, y, project.link)
            pdf.setFillColor(preto)
            y -= 18
        pdf.setFont("Helvetica", 11)
        if y < 100:
            pdf.showPage()
            y = height - 100

    # Rodapé
    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(cinza_texto)
    pdf.drawString(2 * cm, 1.5 * cm, "Gerado automaticamente por DevLink - Seu portfólio inteligente 🚀")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": f"inline; filename=Curriculo_{user_data.name}.pdf"
    })

@router.post("/public/toggle")
def toggle_public_portfolio(db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    db_user.is_public = not db_user.is_public
    db.commit()
    db.refresh(db_user)

    return {
        "message": "Visibilidade alterada com sucesso.",
        "is_public": db_user.is_public,
        "public_link": f"http://127.0.0.1:8000/portfolio/public/{db_user.public_id}" if db_user.is_public else None
    }


@router.get("/public/{public_id}", response_class=HTMLResponse)
def get_public_portfolio(public_id: str, db: Session = Depends(database.get_db)):
    # busca usuário com esse public_id e com portfólio público ativo
    user = db.query(models.User).filter(
        models.User.public_id == public_id,
        models.User.is_public == True
    ).first()

    if not user:
        return HTMLResponse(
            "<h2 style='font-family:sans-serif; text-align:center;'>❌ Este portfólio não está disponível.</h2>",
            status_code=404
        )

    # coleta dados públicos
    skills = db.query(models.Skill).filter(models.Skill.user_id == user.id).all()
    projects = db.query(models.Project).filter(models.Project.user_id == user.id).all()

    # renderiza o template com o mesmo layout do portfólio Angular
    template = env.get_template("portfolio.html")
    html = template.render(user=user, skills=skills, projects=projects)
    return HTMLResponse(content=html)
