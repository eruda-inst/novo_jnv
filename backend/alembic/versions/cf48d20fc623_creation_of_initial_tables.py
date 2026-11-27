"""creation of initial tables

Revision ID: cf48d20fc623
Revises:
Create Date: 2026-11-27 10:10:11.339854

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cf48d20fc623"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("full_name", sa.String, index=True, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean,
            server_default=sa.text("true"),
            index=True,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), onupdate=sa.func.now()),
        if_not_exists=True,
    )
    # Active refresh tokens
    op.create_table(
        "active_refresh_tokens",
        sa.Column("jti", sa.String, primary_key=True),
        sa.Column(
            "expires_at", sa.TIMESTAMP(timezone=True), nullable=False, index=True
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        if_not_exists=True,
    )
    # Permissions
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False, unique=True),
        sa.Column("code", sa.String, nullable=False, unique=True),
        sa.Column("description", sa.String),
        sa.Column(
            "is_active",
            sa.Boolean,
            server_default=sa.text("true"),
            index=True,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), onupdate=sa.func.now()),
        if_not_exists=True,
    )
    # Revoked access tokens
    op.create_table(
        "revoked_access_tokens",
        sa.Column("jti", sa.String, primary_key=True),
        sa.Column(
            "expires_at", sa.TIMESTAMP(timezone=True), nullable=False, index=True
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        if_not_exists=True,
    )
    # Roles
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String, nullable=False, unique=True),
        sa.Column("name", sa.String, nullable=False, unique=True),
        sa.Column("description", sa.String),
        sa.Column(
            "is_active",
            sa.Boolean,
            server_default=sa.text("true"),
            index=True,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), onupdate=sa.func.now()),
        if_not_exists=True,
    )
    # Roles and permissions
    op.create_table(
        "roles_permissions",
        sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id"), primary_key=True),
        sa.Column(
            "permission_id",
            sa.Integer,
            sa.ForeignKey("permissions.id"),
            primary_key=True,
        ),
        if_not_exists=True,
    )
    # Users and roles
    op.create_table(
        "users_roles",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id"), primary_key=True),
        if_not_exists=True,
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS active_refresh_tokens;")
    op.execute("DROP TABLE IF EXISTS revoked_access_tokens;")
    op.execute("DROP TABLE IF EXISTS users CASCADE;")
    op.execute("DROP TABLE IF EXISTS users_roles;")
    op.execute("DROP TABLE IF EXISTS roles_permissions;")
    op.execute("DROP TABLE IF EXISTS roles;")
    op.execute("DROP TABLE IF EXISTS permissions;")
