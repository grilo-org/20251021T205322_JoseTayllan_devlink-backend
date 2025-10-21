from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ importa o Base do seu projeto
from app.database import Base
from app import models  # garante que todas as tabelas estão registradas

# Carrega config do Alembic
config = context.config

# Configura logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ adiciona a metadata usada para autogerar
target_metadata = Base.metadata


def run_migrations_offline():
    """Executa as migrações no modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Executa as migrações no modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
