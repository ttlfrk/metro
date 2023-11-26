"""Init

Revision ID: 0e82b88bfdf4
Revises:
Create Date: 2023-11-25 19:20:53.643077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e82b88bfdf4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Create table brands
    op.create_table(
        'brands',
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            'site_id',
            sa.String(255),
            nullable=False,
        ),
        sa.Column(
            'name',
            sa.String(length=255),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name='brands__id__pkey',
        ),
        sa.UniqueConstraint(
            'name', 'site_id',
            name='brands__name__site_id__unique',
        ),
        sa.CheckConstraint(
            sqltext='LENGTH(name) > 0',
            name='brands__name__check',
        ),
        sa.CheckConstraint(
            sqltext='LENGTH(site_id) > 0',
            name='brands__site_id__check',
        ),
    )

    # Create table products
    op.create_table(
        'products',
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
        sa.Column(
            'store_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'site_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'article',
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            'slug',
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            'name',
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            'price',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'old_price',
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            'brand_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name='products__id__pkey',
        ),
        sa.UniqueConstraint(
            'site_id', 'store_id',
            name='products__site_id__store_id__unique',
        ),
        sa.CheckConstraint(
            sqltext='LENGTH(name) > 0',
            name='products__name__check',
        ),
        sa.CheckConstraint(
            sqltext='LENGTH(name) > 0',
            name='products__slug__check',
        ),
        sa.CheckConstraint(
            sqltext='price > 0',
            name='products__price__check',
        ),
        sa.CheckConstraint(
            sqltext='article > 0',
            name='products__article__check',
        ),
        sa.CheckConstraint(
            sqltext='old_price IS null OR old_price > 0',
            name='products__old_price__check',
        ),
        sa.ForeignKeyConstraint(
            columns=['brand_id'],
            refcolumns=['brands.id'],
            ondelete='RESTRICT',
        ),
    )


def downgrade() -> None:
    op.drop_table('products')
    op.drop_table('brands')
