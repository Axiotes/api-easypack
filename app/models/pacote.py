from __future__ import annotations

from sqlalchemy import CHAR, BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Pacote(Base):
    __tablename__ = "pacote"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    id_correcao: Mapped[int] = mapped_column(BigInteger, ForeignKey("correcao.id"), nullable=False)
    sn_aplicado: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    tp_pacote: Mapped[int] = mapped_column(BigInteger, nullable=False)
    nm_pacote: Mapped[str] = mapped_column(String(255), nullable=False)
    sn_aprovado_usu: Mapped[str | None] = mapped_column(CHAR(1), nullable=True)
    sn_aprovado_gerente: Mapped[str] = mapped_column(CHAR(1), nullable=False)

    correcao: Mapped["Correcao"] = relationship(back_populates="pacotes")
