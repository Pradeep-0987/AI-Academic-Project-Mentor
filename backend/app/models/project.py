import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.database.session import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    domain: Mapped[str | None] = mapped_column(String(160), nullable=True)
    department: Mapped[str | None] = mapped_column(String(255), nullable=True)
    technology_stack: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_weeks: Mapped[int] = mapped_column(Integer, nullable=False, default=8, server_default="8")
    team_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    guide_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="submitted", server_default="submitted")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.current_timestamp())

    student = relationship("User")