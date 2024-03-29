"""Add column skill for table 'worker'

Revision ID: acb022077356
Revises: e1e0fda1aab6
Create Date: 2024-03-18 17:27:48.568434

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "acb022077356"
down_revision: Union[str, None] = "e1e0fda1aab6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("worker", sa.Column("skill", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("worker", "skill")
    # ### end Alembic commands ###
