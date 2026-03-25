from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Project(Base):
	__tablename__ = "projects"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

	owner: Mapped["User"] = relationship(back_populates="projects")


class ProjectMetric(Base):
	__tablename__ = "project_metrics"

	project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
	name: Mapped[str] = mapped_column(String(255))
	value: Mapped[float] = mapped_column()
	unit: Mapped[str] = mapped_column(String(64))
	year: Mapped[int] = mapped_column()
	confidence_score: Mapped[float] = mapped_column()
	source_fragment: Mapped[str] = mapped_column(String(512))
