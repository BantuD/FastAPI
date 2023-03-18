"""Create user table

Revision ID: 2a1c2036f2b5
Revises: 0248d1b3344f
Create Date: 2023-03-18 15:27:17.167113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a1c2036f2b5'
down_revision = '0248d1b3344f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(), nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('NOW()') ,nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
