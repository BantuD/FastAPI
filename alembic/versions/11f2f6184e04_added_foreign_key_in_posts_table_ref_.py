"""Added foreign_key in posts table ref-users

Revision ID: 11f2f6184e04
Revises: 2a1c2036f2b5
Create Date: 2023-03-18 15:58:41.715947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11f2f6184e04'
down_revision = '2a1c2036f2b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owners_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table='users',
                          local_cols=['owners_id'],remote_cols=['id'], ondelete='CASCADE')
    
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts', 'owners_id')

    pass
