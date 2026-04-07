from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models
from app.db.database import Base
from app.models.model import URL

# Metadata for Alembic
target_metadata = Base.metadata


# 🔹 Offline migrations
def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# 🔹 Online migrations
def run_migrations_online() -> None:
    connectable = create_engine(DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Run appropriate mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()