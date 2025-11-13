"""add users table

Revision ID: a99c2bfdaf8f
Revises: b12a66d76848
Create Date: 2025-11-13 10:56:10.220104

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a99c2bfdaf8f'
down_revision: Union[str, Sequence[str], None] = 'b12a66d76848'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create users table"""
    op.create_table("users",
                    sa.Column("id", sa.INTEGER(), nullable=False, autoincrement=True),
                    sa.Column("email", sa.VARCHAR(), nullable=False, unique=True),
                    sa.Column("username", sa.VARCHAR(), nullable=False, unique=True),
                    sa.Column("first_name", sa.VARCHAR()),
                    sa.Column("last_name", sa.VARCHAR()),
                    sa.Column("hashed_password", sa.VARCHAR(), nullable=False),
                    sa.Column("is_active", sa.BOOLEAN(), default=True),
                    sa.Column("role", sa.VARCHAR()),
                    sa.PrimaryKeyConstraint("id", name=op.f("pkey_users"))
                    )


def downgrade() -> None:
    op.drop_table("users")
