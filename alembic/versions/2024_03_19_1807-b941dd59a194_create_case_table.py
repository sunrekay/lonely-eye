"""Create 'case' table

Revision ID: b941dd59a194
Revises: acb022077356
Create Date: 2024-03-19 18:07:32.470984

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b941dd59a194"
down_revision: Union[str, None] = "acb022077356"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "case",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("transport_id", sa.Integer(), nullable=False),
        sa.Column("violation_id", sa.Uuid(), nullable=False),
        sa.Column("violation_value", sa.String(), nullable=False),
        sa.Column("photo_id", sa.Uuid(), nullable=False),
        sa.Column("skill", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["transport_id"],
            ["transport.id"],
        ),
        sa.ForeignKeyConstraint(
            ["violation_id"],
            ["violation.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("photo_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("case")
    # ### end Alembic commands ###
