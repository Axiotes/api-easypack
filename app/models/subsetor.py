from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Subsetor(Base):
    __tablename__ = "subsetor"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    id_setor: Mapped[int] = mapped_column(BigInteger, ForeignKey("setor.id"), nullable=False)
    nm_subsetor: Mapped[str] = mapped_column(String(255), nullable=False)
    id_produto: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("produto.id"), nullable=True)

    setor: Mapped["Setor"] = relationship(back_populates="subsetores")
    produto: Mapped["Produto | None"] = relationship(back_populates="subsetores")
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="subsetor")
