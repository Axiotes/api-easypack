from __future__ import annotations

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TipoPacote(Base):
    __tablename__ = "tipo_pacote"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    nm_tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    nm_grupo: Mapped[str] = mapped_column(String(20), nullable=False)

    pacotes: Mapped[list["Pacote"]] = relationship(back_populates="tipo_pacote")
