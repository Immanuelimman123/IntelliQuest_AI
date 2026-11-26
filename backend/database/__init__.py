from backend.database.db import Base, engine
from backend.database.models import Document


def init_db():
    Base.metadata.create_all(bind=engine)