"""Added vehicle models

Revision ID: 67529bb2b6ea
Revises: 766087f642ad
Create Date: 2023-08-07 12:52:48.881521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "67529bb2b6ea"
down_revision: Union[str, None] = "766087f642ad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # brands table
    op.create_table(
        "brands",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, unique=True, index=True),
    )

    # models table
    op.create_table(
        "models",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, index=True),
        sa.Column("brand_id", sa.Integer, sa.ForeignKey("brands.id")),
    )

    # years table
    op.create_table(
        "years",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, index=True),
        sa.Column("model_id", sa.Integer, sa.ForeignKey("models.id")),
    )

    # vehicle_values table
    op.create_table(
        "vehicle_values",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("type_vehicle", sa.Integer),
        sa.Column("value", sa.String),
        sa.Column("brand", sa.String),
        sa.Column("model", sa.String),
        sa.Column("year_model", sa.Integer),
        sa.Column("fuel", sa.String),
        sa.Column("code_fipe", sa.String),
        sa.Column("month_reference", sa.String),
        sa.Column("sigla_fuel", sa.String),
        sa.Column("year_id", sa.Integer, sa.ForeignKey("years.id")),
    )


def downgrade():
    op.drop_table("vehicle_values")
    op.drop_table("years")
    op.drop_table("models")
    op.drop_table("brands")
