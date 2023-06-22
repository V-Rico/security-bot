"""initial

Revision ID: 3611bb3d9dd2
Revises: 
Create Date: 2023-05-31 12:53:57.376066

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3611bb3d9dd2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "repository_security_check",
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("external_id", sa.String(), nullable=False),
        sa.Column(
            "event_type",
            sa.Enum("PUSH", "TAG_PUSH", "MERGE_REQUEST", name="gitlabevent"),
            nullable=False,
        ),
        sa.Column(
            "event_json", postgresql.JSON(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("commit_hash", sa.String(), nullable=False),
        sa.Column("branch", sa.String(), nullable=False),
        sa.Column("project_name", sa.String(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("prefix", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("external_id"),
    )
    op.create_table(
        "repository_security_scan",
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("check_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("NEW", "IN_PROGRESS", "SKIP", "ERROR", "DONE", name="scanstatus"),
            nullable=False,
        ),
        sa.Column("response", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("scan_name", sa.String(), nullable=False),
        sa.Column(
            "outputs_test_id", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["check_id"],
            ["repository_security_check.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "slack_notifications",
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("channel", sa.String(), nullable=False),
        sa.Column("is_sent", sa.Boolean(), nullable=True),
        sa.Column("payload", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("scan_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["scan_id"],
            ["repository_security_scan.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("slack_notifications")
    op.drop_table("repository_security_scan")
    op.drop_table("repository_security_check")
    # ### end Alembic commands ###
