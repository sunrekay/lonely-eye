"""Create table 'violation'

Revision ID: ac055ab6c176
Revises: 054526761bcc
Create Date: 2024-03-14 16:52:13.736139

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ac055ab6c176"
down_revision: Union[str, None] = "054526761bcc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "violation",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("type", sa.String(length=500), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("type"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("violation")
    # ### end Alembic commands ###
