"""Add item_id unique constraint

Revision ID: bff62620fe69
Revises: f9c5e7ea46c2
Create Date: 2020-10-19 03:54:21.796458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bff62620fe69'
down_revision = 'f9c5e7ea46c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'item_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_foreign_key(None, 'accounts', 'items', ['item_id'], ['item_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'accounts', type_='foreignkey')
    op.alter_column('accounts', 'item_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###