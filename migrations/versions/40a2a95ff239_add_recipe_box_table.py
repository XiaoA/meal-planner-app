"""add recipe_box table

Revision ID: 40a2a95ff239
Revises: 4bef250af75a
Create Date: 2021-06-23 06:00:54.702324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40a2a95ff239'
down_revision = '4bef250af75a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe_boxes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_liked', sa.Boolean(), nullable=False),
    sa.Column('recipe_url', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe_boxes')
    # ### end Alembic commands ###