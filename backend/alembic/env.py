import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Adjust sys.path for both dev (repo root) and installed package (container)
ALEMBIC_DIR = os.path.abspath(os.path.dirname(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(ALEMBIC_DIR, ".."))  # .../backend
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))  # .../
for p in (PROJECT_ROOT, BACKEND_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

# Import settings and metadata; support both 'backend.app.*' (dev) and 'app.*' (installed)
try:  # dev path
    from backend.app.core.config import settings  # type: ignore
    from backend.app.db.base import Base  # type: ignore
    from backend.app.db import models as _models  # noqa: F401
except ModuleNotFoundError:  # installed package path
    from app.core.config import settings  # type: ignore
    from app.db.base import Base  # type: ignore
    from app.db import models as _models  # noqa: F401


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# set DB URL from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
