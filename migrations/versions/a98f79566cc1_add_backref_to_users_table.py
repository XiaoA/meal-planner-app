"""add backref to users table

Revision ID: a98f79566cc1
Revises: e2df3036baa1
Create Date: 2021-07-10 16:57:39.488605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a98f79566cc1'
down_revision = 'e2df3036baa1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('follows', 'user_following_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=False)
    op.alter_column('follows', 'user_being_followed_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('follows', 'user_being_followed_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=False)
    op.alter_column('follows', 'user_following_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=False)
    # ### end Alembic commands ###