from __future__ import annotations

import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from todo_app.config import settings
from todo_app.db.base import Base
from todo_app.db import models as orm_models  # noqa: F401  -> For registering ORM models

# This config comes from the alembic.ini file
config = context.config

# Set the database URL from settings (instead of hardcoding in alembic.ini)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Logging settings
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# This metadata is the source for autogenerate (all classes inheriting from Base)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode (only generate SQL without connecting to the DB)."""
    url = settings.DATABASE_URL

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode (with actual connection to the database)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
