from datetime import datetime

from sqlalchemy import BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class URL:
    __tablename__ = 'urls'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    short_url: Mapped[str] = mapped_column(unique=True)
    original_url: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    access_count: Mapped[int] = mapped_column(init=False, default=0)
