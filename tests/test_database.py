
from sqlalchemy import inspect

from backend.database import init_db
from backend.database.db import engine, SessionLocal
from backend.database.models import Document


def main():

    print("\n========== INTELLIQUEST DATABASE TEST ==========")

    # Initialize database
    init_db()

    print("\nDatabase initialized successfully!")

    # Check database tables
    inspector = inspect(engine)

    tables = inspector.get_table_names()

    print("\nAvailable Tables:")

    for table in tables:
        print("-", table)

    # Test database connection
    db = SessionLocal()

    try:
        total_documents = db.query(Document).count()

        print("\nDatabase Connection: Successful")
        print("Total Documents:", total_documents)

    finally:
        db.close()

    print("\nDatabase Path:")
    print(engine.url.database)

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    main()
