
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    BigInteger,
    UniqueConstraint
)

from backend.database.db import Base


class Document(Base):

    __tablename__ = "documents"

    __table_args__ = (
        UniqueConstraint(
            "filename",
            "content_hash",
            name="uq_document_filename_hash"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    filename = Column(
        String(255),
        nullable=False
    )

    content_hash = Column(
        String(64),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=True
    )

    file_size = Column(
        BigInteger,
        default=0
    )

    total_pages = Column(
        Integer,
        default=0
    )

    total_chunks = Column(
        Integer,
        default=0
    )

    status = Column(
        String(50),
        default="pending"
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
