"""Add dodopayments_customer_id to users table.

Revision ID: b2c3d4e5f6a7
Revises: 7e28cabbd659
Create Date: 2026-02-19

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b2c3d4e5f6a7"
down_revision = "7e28cabbd659"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("dodopayments_customer_id", sa.String(255), nullable=True),
    )
    op.create_index(
        "idx_users_dodopayments_customer",
        "users",
        ["dodopayments_customer_id"],
    )


def downgrade() -> None:
    op.drop_index("idx_users_dodopayments_customer", table_name="users")
    op.drop_column("users", "dodopayments_customer_id")
