"""Create tables 'car_owner' and 'transport'

Revision ID: 054526761bcc
Revises: dcb0cf78bdc4
Create Date: 2024-03-13 20:12:44.370794

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "054526761bcc"
down_revision: Union[str, None] = "dcb0cf78bdc4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "car_owner",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("vk", sa.String(), nullable=True),
        sa.Column("telegram", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone"),
        sa.UniqueConstraint("telegram"),
        sa.UniqueConstraint("vk"),
    )
    op.create_table(
        "transport",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("number", sa.String(length=15), nullable=False),
        sa.Column("car_owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["car_owner_id"],
            ["car_owner.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("number"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transport")
    op.drop_table("car_owner")
    # ### end Alembic commands ###