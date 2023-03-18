"""Create post table

Revision ID: ba8dc6b196d7
Revises: 
Create Date: 2023-03-17 12:01:23.754383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba8dc6b196d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),primary_key=True,nullable=False),
                    sa.Column('title',sa.String(),nullable=False))
    
    pass


def downgrade():
    op.drop_table('posts')
    pass
