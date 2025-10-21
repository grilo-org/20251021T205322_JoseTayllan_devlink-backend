from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database
from app.routes import auth, users, skills, projects, portfolio

from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 🔹 Configurar CORS
origins = [
    "http://localhost:4200",   # Angular local
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # quais origens podem chamar
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, PUT, DELETE, OPTIONS...
    allow_headers=["*"],        # permite todos os headers
)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(skills.router)
app.include_router(projects.router)
app.include_router(portfolio.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/health")
def health_check():
    return {"status": "ok"}
