"""add todos table

Revision ID: b12a66d76848
Revises: 
Create Date: 2025-11-13 10:35:27.191309

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b12a66d76848'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create todos table"""
    op.create_table("todos",
    sa.Column("id", sa.INTEGER(), nullable=False, autoincrement=True),
             sa.Column("title", sa.VARCHAR(), nullable=False),
             sa.Column("description", sa.VARCHAR(), nullable=True),
             sa.Column("priority", sa.INTEGER(), nullable=False, default=5),
             sa.Column("complete", sa.BOOLEAN(), nullable=False, default=False),
             sa.PrimaryKeyConstraint("id", name=op.f("pkey_todos"))
             )



def downgrade() -> None:
    op.drop_table("todos")
