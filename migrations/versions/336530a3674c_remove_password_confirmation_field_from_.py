"""remove password confirmation field from users

Revision ID: 336530a3674c
Revises: 9da07c087f15
Create Date: 2021-06-13 08:43:20.251846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '336530a3674c'
down_revision = '9da07c087f15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_confirmation_hashed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_confirmation_hashed', sa.VARCHAR(length=264), autoincrement=False, nullable=False))
    # ### end Alembic commands ###