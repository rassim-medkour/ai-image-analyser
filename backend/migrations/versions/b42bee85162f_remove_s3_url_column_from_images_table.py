"""Remove s3_url column from images table

Revision ID: b42bee85162f
Revises: 36e2aa5033aa
Create Date: 2025-04-29 11:27:25.271117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b42bee85162f'
down_revision = '36e2aa5033aa'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.drop_column('s3_url')


def downgrade():
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.add_column(sa.Column('s3_url', sa.VARCHAR(length=512), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
