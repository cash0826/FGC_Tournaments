"""Make standings one-to-one with tournament competitors.

Revision ID: 2a7c4e1d9b63
Revises: 89f4a05b28a8
Create Date: 2026-10-08 17:55:17.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2a7c4e1d9b63"
down_revision = "89f4a05b28a8"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    missing_competitors = connection.execute(
        sa.text(
            "SELECT COUNT(*) FROM standings "
            "WHERE tournament_competitor_id IS NULL"
        )
    ).scalar_one()
    duplicate_competitors = connection.execute(
        sa.text(
            "SELECT COUNT(*) FROM ("
            "SELECT tournament_competitor_id FROM standings "
            "GROUP BY tournament_competitor_id HAVING COUNT(*) > 1"
            ")"
        )
    ).scalar_one()
    if missing_competitors or duplicate_competitors:
        raise RuntimeError(
            "Cannot enforce one-to-one standings: remove standings without a "
            "competitor and resolve duplicate standings before upgrading."
        )

    with op.batch_alter_table("standings", schema=None) as batch_op:
        batch_op.alter_column(
            "tournament_competitor_id",
            existing_type=sa.Integer(),
            nullable=False,
        )
        batch_op.create_unique_constraint(
            "uq_standings_tournament_competitor",
            ["tournament_competitor_id"],
        )


def downgrade():
    with op.batch_alter_table("standings", schema=None) as batch_op:
        batch_op.drop_constraint(
            "uq_standings_tournament_competitor",
            type_="unique",
        )
        batch_op.alter_column(
            "tournament_competitor_id",
            existing_type=sa.Integer(),
            nullable=True,
        )
