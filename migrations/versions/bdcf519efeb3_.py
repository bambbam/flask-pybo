"""empty message

Revision ID: bdcf519efeb3
Revises: f17125472b75
Create Date: 2020-12-24 16:27:29.208453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdcf519efeb3'
down_revision = 'f17125472b75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq_user_email'), 'user', ['email'])
    op.create_unique_constraint(op.f('uq_user_user_name'), 'user', ['user_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_user_user_name'), 'user', type_='unique')
    op.drop_constraint(op.f('uq_user_email'), 'user', type_='unique')
    # ### end Alembic commands ###