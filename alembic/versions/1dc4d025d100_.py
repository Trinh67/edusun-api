"""empty message

Revision ID: 1dc4d025d100
Revises: 16885484f1dc
Create Date: 2023-10-02 23:40:08.645110

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1dc4d025d100'
down_revision = '16885484f1dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('fullname', sa.Unicode(length=255), nullable=False),
    sa.Column('year_of_birth', sa.SmallInteger(), nullable=True),
    sa.Column('address', sa.Unicode(length=255), nullable=True),
    sa.Column('phone_number', sa.Unicode(length=255), nullable=True),
    sa.Column('email', sa.Unicode(length=255), nullable=True),
    sa.Column('average_graduation_score', sa.Float(), nullable=True),
    sa.Column('parent_name', sa.Unicode(length=255), nullable=True),
    sa.Column('parent_phone_number', sa.Unicode(length=255), nullable=True),
    sa.Column('graduation_type', sa.Unicode(length=255), nullable=True),
    sa.Column('interested', sa.Unicode(length=255), nullable=True),
    sa.Column('note', sa.Unicode(length=255), nullable=True),
    sa.Column('attachment_url', sa.Unicode(length=1024), nullable=True),
    sa.Column('contact_name', sa.Unicode(length=255), nullable=True),
    sa.Column('contact_phone_number', sa.Unicode(length=255), nullable=True),
    sa.Column('expected_admission', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Unicode(length=32), nullable=False),
    sa.Column('rejected_reason', sa.Unicode(length=255), nullable=True),
    sa.Column('failed_reason', sa.Unicode(length=255), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('deleted_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('phone_number', sa.Unicode(length=255), nullable=False))
    op.drop_index('phone', table_name='user')
    op.create_unique_constraint(None, 'user', ['phone_number'])
    op.drop_column('user', 'phone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone', mysql.VARCHAR(length=255), nullable=False))
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('phone', 'user', ['phone'], unique=False)
    op.drop_column('user', 'phone_number')
    op.drop_table('candidate')
    # ### end Alembic commands ###
