from __future__ import annotations

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Produto(Base):
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    nm_produto: Mapped[str] = mapped_column(String(255), nullable=False)

    subsetores: Mapped[list["Subsetor"]] = relationship(back_populates="produto")
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="produto")
    correcoes: Mapped[list["Correcao"]] = relationship(back_populates="produto")
