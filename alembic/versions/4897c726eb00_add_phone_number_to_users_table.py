"""add phone_number to users table

Revision ID: 4897c726eb00
Revises: 978b77f6be84
Create Date: 2025-11-13 11:55:50.729805

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4897c726eb00'
down_revision: Union[str, Sequence[str], None] = '978b77f6be84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.VARCHAR(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
