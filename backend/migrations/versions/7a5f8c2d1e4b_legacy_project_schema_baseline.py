"""Recognize the legacy deployed project schema revision.

Revision ID: 7a5f8c2d1e4b
Revises: 3842d0348391
"""
from typing import Sequence, Union


revision: str = "7a5f8c2d1e4b"
down_revision: Union[str, None] = "3842d0348391"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
