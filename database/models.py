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
            name='brands__name__check',
        )
    )

    # Columns
    id: Mapped[int] = mapped_column(
        Integer(),
        autoincrement=True,
    )
    site_id: Mapped[str] = mapped_column(
        Integer(),
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
            name='products__name__check',
        ),
        CheckConstraint(
            sqltext='LENGTH(name) > 2',
            name='products__slug__check',
        ),
        CheckConstraint(
            sqltext='price > 0',
            name='products__price__check',
        ),
        CheckConstraint(
            sqltext='old_price IS null OR old_price > 0',
            name='products__old_price__check',
        ),
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
        Integer(),
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

    brand_id: Mapped[int] = mapped_column(
        ForeignKey(
            column=Brand.id,
            ondelete='RESTRICT',
        ),
    )
    brand: Mapped[Brand] = relationship(
        back_populates='products',
    )
