"""Add unique constraint to user roles.

Revision ID: 7f2c1d4a8e91
Revises: 3b09ee5fb004
Create Date: 2026-09-23 17:45:07.164809

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "7f2c1d4a8e91"
down_revision = "3b09ee5fb004"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user_roles", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            "uq_user_roles_user_role", ["user_id", "role_id"]
        )


def downgrade():
    with op.batch_alter_table("user_roles", schema=None) as batch_op:
        batch_op.drop_constraint("uq_user_roles_user_role", type_="unique")
