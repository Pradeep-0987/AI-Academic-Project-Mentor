import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.database.session import Base


class ProjectBlueprint(Base):
    __tablename__ = "project_blueprints"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    feasibility: Mapped[dict] = mapped_column(JSON, nullable=False)
    scope: Mapped[dict] = mapped_column(JSON, nullable=False)
    technology: Mapped[dict] = mapped_column(JSON, nullable=False)
    planning: Mapped[dict] = mapped_column(JSON, nullable=False)
    risk: Mapped[dict] = mapped_column(JSON, nullable=False)
    quality_report: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, server_default=func.current_timestamp(), onupdate=datetime.utcnow
    )

    project = relationship("Project", backref="blueprint")
