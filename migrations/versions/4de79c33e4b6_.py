"""empty message

Revision ID: 4de79c33e4b6
Revises: 389b6ef8af0a
Create Date: 2021-06-13 22:40:51.372140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4de79c33e4b6'
down_revision = '389b6ef8af0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verification_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('data', sa.PickleType(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('request_date', sa.Date(), nullable=False),
    sa.Column('verification_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verification_data')
    # ### end Alembic commands ###
