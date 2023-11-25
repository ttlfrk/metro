import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy import CheckConstraint
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.connect import Base


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='categories__id__pkey',
        ),
        UniqueConstraint(
            'name', 'parent_id',
            name='categories__name__parent_id__unique',
        ),
        CheckConstraint(
            sqltext='LENGTH(name) > 2',
            name='categories__name__check',
        ),
    )

    # Columns
    id: Mapped[int] = mapped_column(
        Integer(),
        autoincrement=True,
    )
    site_id: Mapped[int] = mapped_column(
        Integer(),
    )
    slug: Mapped[str] = mapped_column(
        String(255),
    )
    name: Mapped[str] = mapped_column(
        String(255),
    )

    # Relationships
    parent_id: Mapped[int] = mapped_column(
        ForeignKey(
            column='categories.id',
            ondelete='RESTRICT',
            name='categories__parent_id__fkey',
        ),
    )
    parent: Mapped['Category'] = relationship(
        'Category',
        back_populates='childs',
        remote_side=[id],
    )
    childs: Mapped[List['Category']] = relationship(
        back_populates='parent',
    )
    products: Mapped[List['Product']] = relationship(
        back_populates='category',
    )


class Brand(Base):
    __tablename__ = 'brands'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='brands__id__pkey',
        ),
        UniqueConstraint(
            'name',
            name='brands__name__unique',
        ),
        CheckConstraint(
            sqltext='LENGTH(name) > 2',
            name='categories__name__check',
        )
    )

    # Columns
    id: Mapped[int] = mapped_column(
        Integer(),
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
    )

    # Relations
    products: Mapped[List['Product']] = relationship(
        back_populates='brand',
    )


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='products__id__pkey',
        ),
        UniqueConstraint(
            'site_id',
            name='products__site_id__unique',
        ),
        CheckConstraint(
            sqltext='LENGTH(name) > 2',
            name='categories__name__check',
        )
    )

    # Columns
    id: Mapped[int] = mapped_column(
        Integer(),
        autoincrement=True,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
    site_id: Mapped[str] = mapped_column(
        String(255),
    )
    article: Mapped[int] = mapped_column(
        Integer(),
    )
    slug: Mapped[str] = mapped_column(
        String(255)
    )
    name: Mapped[str] = mapped_column(
        String(255),
    )
    price: Mapped[int] = mapped_column(
        Integer()
    )
    old_price: Mapped[int] = mapped_column(
        Integer(),
        nullable=True,
    )

    # Relations
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=Category.id,
            ondelete='RESTRICT',
        ),
    )
    category: Mapped[Category] = relationship(
        back_populates='products',
    )
    brand_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=Brand.id,
            ondelete='RESTRICT',
        ),
    )
    brand: Mapped[Brand] = relationship(
        back_populates='products',
    )
