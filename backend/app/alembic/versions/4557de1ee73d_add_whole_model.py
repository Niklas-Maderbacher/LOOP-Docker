"""Add Whole Model

Revision ID: 4557de1ee73d
Revises: ccb5d23a21b5
Create Date: 2025-01-27 16:37:25.932943

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '4557de1ee73d'
down_revision = 'ccb5d23a21b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('priority',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sprint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('end_date', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('issue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('sprint_id', sa.Integer(), nullable=True),
    sa.Column('state_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('responsible_user_id', sa.Integer(), nullable=True),
    sa.Column('priority_id', sa.Integer(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('repository_link', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('story_points', sa.Integer(), nullable=True),
    sa.Column('report_time', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('updater_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('backlog_order_number', sa.Integer(), nullable=True),
    sa.Column('deleted_at', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('finisher_id', sa.Integer(), nullable=True),
    sa.Column('parent_issue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['finisher_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['parent_issue_id'], ['issue.id'], ),
    sa.ForeignKeyConstraint(['priority_id'], ['priority.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['responsible_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sprint_id'], ['sprint.id'], ),
    sa.ForeignKeyConstraint(['state_id'], ['state.id'], ),
    sa.ForeignKeyConstraint(['updater_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attachment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('issue_id', sa.Integer(), nullable=False),
    sa.Column('link', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attachment')
    op.drop_table('issue')
    op.drop_table('sprint')
    op.drop_table('state')
    op.drop_table('priority')
    op.drop_table('category')
    # ### end Alembic commands ###
