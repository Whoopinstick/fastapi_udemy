"""add owner_id to todos table and FK to users table

Revision ID: 978b77f6be84
Revises: a99c2bfdaf8f
Create Date: 2025-11-13 11:44:39.062458

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import nullsfirst

# revision identifiers, used by Alembic.
revision: str = '978b77f6be84'
down_revision: Union[str, Sequence[str], None] = 'a99c2bfdaf8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("todos", sa.Column("owner_id", sa.INTEGER(), nullable=False))

    op.create_foreign_key("fk_todos_owner_id_users", "todos",
                          "users", ["owner_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint("fk_todos_owner_id_users", "todos", "foreignkey")
    op.drop_column("todos", "owner_id")
