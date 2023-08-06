"""User table migration

Revision ID: 766087f642ad
Revises: 
Create Date: 2023-08-06 12:17:30.496422

"""
from typing import Sequence, Union

from sqlalchemy import Column, Integer, String

from alembic import op
from app.core.database import Base

# revision identifiers, used by Alembic.
revision: str = "766087f642ad"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define the new User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


def upgrade():
    # Create the 'users' table
    op.create_table(
        "users",
        Column("id", Integer, primary_key=True, index=True),
        Column("username", String, unique=True, index=True),
        Column("hashed_password", String),
    )


def downgrade():
    # Drop the 'users' table
    op.drop_table("users")
