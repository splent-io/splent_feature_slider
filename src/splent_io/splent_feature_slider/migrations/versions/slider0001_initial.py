"""slide table (homepage carousel).

Revision ID: slider0001
Revises:
"""

import sqlalchemy as sa
from alembic import op

revision = "slider0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "slide",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("media_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("link", sa.String(length=512), nullable=True),
        sa.Column("order", sa.Integer(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["media_id"], ["media_item.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_slide_media_id"), "slide", ["media_id"])
    op.create_index(op.f("ix_slide_order"), "slide", ["order"])
    op.create_index(op.f("ix_slide_active"), "slide", ["active"])


def downgrade():
    op.drop_index(op.f("ix_slide_active"), table_name="slide")
    op.drop_index(op.f("ix_slide_order"), table_name="slide")
    op.drop_index(op.f("ix_slide_media_id"), table_name="slide")
    op.drop_table("slide")
