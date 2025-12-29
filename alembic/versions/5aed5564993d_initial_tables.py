"""initial tables

Revision ID: 5aed5564993d
Revises:
Create Date: 2025-12-29 18:34:05.433302
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String, Boolean


# revision identifiers, used by Alembic.
revision: str = "5aed5564993d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Tabla virtual para seed
users_table = table(
    "users",
    column("id", Integer),
    column("username", String),
    column("email", String),
    column("password", String),
    column("is_active", Boolean),
)


def upgrade() -> None:
    """Upgrade schema."""

    # === USERS ===
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )

    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    # === SEED ADMIN USER ===
    op.bulk_insert(
        users_table,
        [
            {
                "id": 1,
                "username": "admin",
                "email": "admin@admin.com",
                "password": "$argon2id$v=19$m=65536,t=3,p=4$JuRcizGm9P6f0/pfy/k/Rw$Kw/RTy8seCQPsADetq8SdkQpIkGn4fyU4aED7HBUBgY",
                "is_active": True,
            }
        ],
    )

    # === TASKS ===
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(op.f("ix_tasks_id"), "tasks", ["id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""

    op.execute("DELETE FROM users WHERE email = 'admin@admin.com'")

    op.drop_index(op.f("ix_tasks_id"), table_name="tasks")
    op.drop_table("tasks")

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
