from __future__ import annotations

from sqlalchemy import CHAR, BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Correcao(Base):
    __tablename__ = "correcao"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    ticket: Mapped[str] = mapped_column(String(100), nullable=False)
    ticket_bug: Mapped[str | None] = mapped_column(String(100), nullable=True)
    merge: Mapped[str | None] = mapped_column(String(255), nullable=True)
    id_cliente: Mapped[int] = mapped_column(BigInteger, ForeignKey("cliente.id"), nullable=False)
    id_produto: Mapped[int] = mapped_column(BigInteger, ForeignKey("produto.id"), nullable=False)
    id_usuario: Mapped[int] = mapped_column(BigInteger, ForeignKey("usuario.id"), nullable=False)
    id_setor: Mapped[int] = mapped_column(BigInteger, ForeignKey("setor.id"), nullable=False)
    sn_mergeado: Mapped[str | None] = mapped_column(CHAR(1), nullable=True)
    versao_correcao: Mapped[str] = mapped_column(String(50), nullable=False)
    sn_aprovado_code_review: Mapped[str] = mapped_column(CHAR(1), nullable=False)

    cliente: Mapped["Cliente"] = relationship(back_populates="correcoes")
    produto: Mapped["Produto"] = relationship(back_populates="correcoes")
    usuario: Mapped["Usuario"] = relationship(back_populates="correcoes")
    setor: Mapped["Setor"] = relationship(back_populates="correcoes")
    pacotes: Mapped[list["Pacote"]] = relationship(back_populates="correcao")
