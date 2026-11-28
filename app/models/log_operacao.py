from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class LogOperacao(Base):
    """Histórico das principais operações do sistema (quem fez o quê, quando)."""

    __tablename__ = "log_operacao"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    dt_operacao: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    id_usuario: Mapped[int] = mapped_column(BigInteger, ForeignKey("usuario.id"), nullable=False)
    nm_usuario: Mapped[str] = mapped_column(String(255), nullable=False)
    nm_entidade: Mapped[str] = mapped_column(String(50), nullable=False)
    id_entidade: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ds_acao: Mapped[str] = mapped_column(String(50), nullable=False)
    ds_detalhe: Mapped[str] = mapped_column(String(500), nullable=False)

    usuario: Mapped["Usuario"] = relationship()
