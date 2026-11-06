"""Add project planning metadata.

Revision ID: 5f41a6d9c2b0
Revises: 3842d0348391
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5f41a6d9c2b0"
down_revision: Union[str, None] = "7a5f8c2d1e4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("domain", sa.String(length=160), nullable=True))
    op.add_column("projects", sa.Column("department", sa.String(length=255), nullable=True))
    op.add_column("projects", sa.Column("technology_stack", sa.Text(), nullable=True))
    op.add_column(
        "projects",
        sa.Column("duration_weeks", sa.Integer(), server_default="8", nullable=False),
    )
    op.add_column("projects", sa.Column("team_size", sa.Integer(), nullable=True))
    op.add_column("projects", sa.Column("guide_name", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("projects", "guide_name")
    op.drop_column("projects", "team_size")
    op.drop_column("projects", "duration_weeks")
    op.drop_column("projects", "technology_stack")
    op.drop_column("projects", "department")
    op.drop_column("projects", "domain")
