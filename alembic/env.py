"""
alembic/env.py

Key changes from the default template:
1. Import `settings` from your config to get the real DATABASE_URL
   (instead of relying only on alembic.ini).
2. Import the `models` package so every table is registered on Base
   BEFORE we hand target_metadata to Alembic — otherwise autogenerate
   will see an empty/partial schema.
3. Set target_metadata = Base.metadata for autogenerate support.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings

# Import the models package (not just Base) so every mapped class
# actually gets registered on Base.metadata as a side effect of import.
import app.models  # noqa: F401
from app.db.base import Base

# this is the Alembic Config object, which provides access to values
# within the .ini file in use.
config = context.config

# Override sqlalchemy.url from alembic.ini with the one from settings/.env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata is what autogenerate diffs your models against
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (generates SQL without a DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (connects to the DB directly)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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