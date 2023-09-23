"""empty message

Revision ID: 7eca65df8aa0
Revises: d6d3d0f966ba
Create Date: 2023-09-23 15:51:56.116068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7eca65df8aa0'
down_revision = 'd6d3d0f966ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('email', sa.Unicode(length=255), nullable=True),
    sa.Column('username', sa.Unicode(length=255), nullable=False),
    sa.Column('password_hash', sa.Unicode(length=255), nullable=True),
    sa.Column('password_encrypted', sa.Unicode(length=255), nullable=True),
    sa.Column('password_reset_hash', sa.Unicode(length=255), nullable=True),
    sa.Column('password_reset_encrypted', sa.Unicode(length=255), nullable=True),
    sa.Column('fullname', sa.Unicode(length=255), nullable=True),
    sa.Column('avatar_url', sa.Unicode(length=1024), nullable=True),
    sa.Column('status', sa.Unicode(length=32), nullable=False),
    sa.Column('type', sa.Unicode(length=32), nullable=False),
    sa.Column('role', sa.Unicode(length=32), nullable=True),
    sa.Column('gender', sa.Unicode(length=32), nullable=True),
    sa.Column('age', sa.SmallInteger(), nullable=True),
    sa.Column('birthday', sa.DateTime(), nullable=True),
    sa.Column('phone', sa.Unicode(length=255), nullable=True),
    sa.Column('address', sa.Unicode(length=255), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('deleted_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_token',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('token', sa.Unicode(length=255), nullable=False),
    sa.Column('expired_at', sa.DateTime(), nullable=False),
    sa.Column('ip_address', sa.Unicode(length=128), nullable=True),
    sa.Column('user_agent', sa.Unicode(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_token')
    op.drop_table('user')
    # ### end Alembic commands ###