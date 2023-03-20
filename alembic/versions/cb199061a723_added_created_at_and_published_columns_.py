"""Added created_at and published columns in <posts> table

Revision ID: cb199061a723
Revises: 11f2f6184e04
Create Date: 2023-03-18 16:12:52.526348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb199061a723'
down_revision = '11f2f6184e04'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                    nullable=False,server_default=sa.text('NOW()')))
    op.add_column('posts',sa.Column('published',sa.Boolean,nullable=False,server_default='TRUE'))

    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')

    pass
