"""set up follows table

Revision ID: 0136ea02909a
Revises: 336530a3674c
Create Date: 2021-06-15 15:11:36.127565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0136ea02909a'
down_revision = '336530a3674c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_following_id', sa.Integer(), nullable=False),
    sa.Column('user_being_followed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_being_followed_id'], ['users.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_following_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id', 'user_following_id', 'user_being_followed_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('follows')
    # ### end Alembic commands ###
