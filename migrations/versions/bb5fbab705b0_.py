"""empty message

Revision ID: bb5fbab705b0
Revises: 68fafa96e5f2
Create Date: 2021-12-07 22:27:11.647778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb5fbab705b0'
down_revision = '68fafa96e5f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('country', schema=None) as batch_op:
        batch_op.drop_column('langx')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('country', schema=None) as batch_op:
        batch_op.add_column(sa.Column('langx', sa.FLOAT(), nullable=True))

    # ### end Alembic commands ###
