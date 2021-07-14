"""add id and unique constraint to follows table

Revision ID: e2df3036baa1
Revises: 08269e1197d0
Create Date: 2021-07-10 12:40:09.495059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2df3036baa1'
down_revision = '08269e1197d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'follows', ['user_following_id', 'user_being_followed_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'follows', type_='unique')
    # ### end Alembic commands ###