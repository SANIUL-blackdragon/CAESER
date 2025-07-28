from alembic import config

def init_db():
    alembic_cfg = config.Config("alembic.ini")
    alembic.command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    init_db()