import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
DB_URL = os.getenv("DB_PATH", "postgresql+asyncpg://caeser_user:caeser_pass@localhost:5432/caeser")

# Alembic Config object
config = context.config
config.set_main_option('sqlalchemy.url', DB_URL)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate support
target_metadata = None

async def run_migrations_online():
    """Run migrations in 'online' mode using async engine."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata
            )
        )
        await connection.run_sync(
            lambda sync_conn: context.run_migrations()
        )

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())