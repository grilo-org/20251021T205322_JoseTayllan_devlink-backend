# 🧠 DevLink Backend – API REST com FastAPI

O **DevLink Backend** é a base da aplicação DevLink, uma plataforma de **portfólios interativos** para desenvolvedores.  
Permite cadastrar usuários, atualizar perfis, gerenciar *skills* e *projetos*, e gerar um **portfólio online e currículo PDF profissional**.

---

## 🚀 Tecnologias, Bibliotecas e Ferramentas Utilizadas

| Categoria           | Nome / Biblioteca           | Descrição / Uso Principal                          |
|---------------------|----------------------------|----------------------------------------------------|
| **Linguagem**       | Python 3.11+                | Base do projeto                                    |
| **Framework**       | FastAPI                     | API REST, validação e documentação automática      |
| **ORM**             | SQLAlchemy                  | Modelagem e acesso ao banco de dados               |
| **Banco de Dados**  | SQLite                      | Banco local padrão                                 |
|                     | PostgreSQL                  | Suporte para produção                              |
| **Migrações**       | Alembic                     | Controle de migrações do banco                     |
| **Autenticação**    | Passlib + Bcrypt            | Hash e validação de senhas                         |
|                     | JWT (python-jose)           | Autenticação segura com tokens                     |
| **PDF**             | ReportLab                   | Geração de PDFs personalizados                     |
| **Templates HTML**  | Jinja2                      | Templates HTML para portfólios públicos            |
| **Server**          | Uvicorn                     | Servidor ASGI de desenvolvimento                   |
| **Uploads**         | FastAPI StaticFiles          | Upload e servir arquivos estáticos                 |
| **Validação**       | Pydantic                    | Schemas e validação de dados                       |
| **Documentação**    | Swagger UI (/docs)          | Interface interativa de documentação               |
|                     | Redoc (/redoc)              | Documentação alternativa                           |
| **Testes**          | Pytest                      | Testes automatizados                               |
| **CI/CD**           | GitHub Actions              | Integração contínua e deploy                       |
| **Outros**          | python-dotenv               | Gerenciamento de variáveis de ambiente             |
|                     | Pillow                      | Manipulação de imagens (upload de perfil)          |
|                     | httpx                       | Requisições HTTP assíncronas                       |
|                     | email-validator             | Validação de e-mails                               |

---

## 🧩 Estrutura de Pastas

```text
devlink-backend/
├── app/
│   ├── main.py                # Ponto de entrada FastAPI
│   ├── models.py              # Modelos do banco (User, Skill, Project)
│   ├── schemas.py             # Schemas Pydantic
│   ├── database.py            # Configuração do SQLAlchemy
│   ├── core/
│   │   └── security.py        # Hash, JWT e autenticação
│   ├── routes/
│   │   ├── auth.py            # Login e registro
│   │   ├── users.py           # Perfil e atualização de usuário
│   │   ├── skills.py          # CRUD de skills
│   │   ├── projects.py        # CRUD de projetos
│   │   └── portfolio.py       # Geração de PDF e portfólio público
│   └── templates/
│       └── portfolio.html     # Template HTML público (Jinja2)
├── migrations/                # Migrações Alembic
├── uploads/                   # Fotos de perfil enviadas
├── README.md                  # (este arquivo)
└── requirements.txt           # Dependências do projeto
```

---

## ⚡️ Instalação Rápida

```bash
# Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate      # (Windows)
source venv/bin/activate   # (Linux/Mac)

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
alembic upgrade head

# Rodar servidor de desenvolvimento
uvicorn app.main:app --reload
```

---

## 🧠 Principais Funcionalidades

| Recurso                | Descrição                                              |
|------------------------|-------------------------------------------------------|
| 🔐 Autenticação JWT    | Registro e login com senhas criptografadas            |
| 👤 Perfil do usuário   | Atualizar nome, cargo, bio e foto                     |
| 🧰 Skills              | Adicionar, listar e remover habilidades               |
| 💼 Projetos            | Adicionar, listar e remover projetos                  |
| 🖼️ Upload de imagem    | Foto de perfil salva localmente                       |
| 📄 Geração de PDF      | Currículo profissional com dados e projetos           |
| 🌍 Portfólio público   | Link público acessível por recrutadores               |
| 🧭 Migrações automáticas| Controle de schema com Alembic                       |

---

## 📡 Principais Rotas da API

### 🔐 Autenticação

| Método | Rota             | Descrição                |
|--------|------------------|--------------------------|
| POST   | /auth/register   | Registrar novo usuário   |
| POST   | /auth/login      | Login com JWT            |

### 👤 Usuário

| Método | Rota             | Descrição                        |
|--------|------------------|----------------------------------|
| GET    | /users/me        | Retorna perfil do usuário logado |
| PUT    | /users/update    | Atualiza nome, cargo, bio e foto |

### 🧰 Skills

| Método | Rota             | Descrição                |
|--------|------------------|--------------------------|
| GET    | /skills          | Lista skills             |
| POST   | /skills          | Adiciona nova skill      |
| DELETE | /skills/{id}     | Remove skill             |

### 💼 Projetos

| Método | Rota             | Descrição                |
|--------|------------------|--------------------------|
| GET    | /projects        | Lista projetos           |
| POST   | /projects        | Adiciona novo projeto    |
| DELETE | /projects/{id}   | Remove projeto           |

### 🌍 Portfólio

| Método | Rota                             | Descrição                        |
|--------|----------------------------------|----------------------------------|
| GET    | /portfolio/html                  | Exibe portfólio em HTML autenticado |
| GET    | /portfolio/pdf                   | Gera PDF profissional            |
| POST   | /portfolio/public/toggle         | Alterna visibilidade pública     |
| GET    | /portfolio/public/{public_id}    | Exibe portfólio público (sem login) |

---

## 🧾 Geração de PDF Profissional

- Desenvolvido com **ReportLab**
- Inclui:
    - Cabeçalho com nome, cargo e foto
    - Bio / resumo profissional
    - Lista de skills e projetos
    - Link para o portfólio online (se público)
- Totalmente automático via `/portfolio/pdf`

---

## 🌐 Portfólio Público (HTML com Jinja2)

- Template moderno em `/app/templates/portfolio.html`
- Renderiza:
    - Nome, foto, cargo e bio do usuário
    - Skills com badges
    - Projetos com descrição e links
- Publicado via link:  
    `http://127.0.0.1:8000/portfolio/public/{public_id}`

---

## 🧰 Ferramentas e Técnicas Usadas

| Categoria         | Tecnologias / Ferramentas         |
|-------------------|-----------------------------------|
| Framework         | FastAPI                           |
| Banco de Dados    | SQLite, PostgreSQL, SQLAlchemy ORM|
| Autenticação      | JWT, Passlib (bcrypt)             |
| Documentação      | Swagger UI, Redoc                 |
| Geração de PDF    | ReportLab                         |
| Templates HTML    | Jinja2                            |
| Migrações         | Alembic                           |
| Uploads           | FastAPI StaticFiles, Pillow       |
| Validação de dados| Pydantic, email-validator         |
| Server            | Uvicorn (ASGI)                    |
| Testes            | Pytest                            |
| CI/CD             | GitHub Actions                    |
| Outros            | python-dotenv, httpx              |

---

## 🔮 Próximos Passos e Possíveis Melhorias

- Criar slug amigável para links públicos (`/u/joaosilva`)
- Adicionar estatísticas de visualização do portfólio
- Permitir temas personalizados no HTML
- Migrar para PostgreSQL em produção
- Implementar envio de e-mails (reset de senha, contato, etc.)
- Hospedar em Render / Railway / Fly.io
- Adicionar testes automatizados com Pytest
- Integração CI/CD com GitHub Actions

---

## 🧑‍💻 Autor

**José Tayllan Pinto Almeida**  
Desenvolvedor em evolução 🚀 | Construindo o portfólio DevLink com FastAPI + Angular

- LinkedIn: [linkedin.com/in/josé-tayllan](https://www.linkedin.com/in/josé-tayllan-241a65298)
- GitHub: [github.com/JoseTayllan](https://github.com/JoseTayllan)
- Portfólio: [jose/portfolio/josé-tayllan](https://portfolio-hub-silk.vercel.app/)
---

## 🏁 Licença

Este projeto está sob a licença MIT — sinta-se livre para usar e adaptar.

