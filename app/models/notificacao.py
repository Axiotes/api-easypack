from __future__ import annotations

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Notificacao(Base):
    __tablename__ = "notificacao"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    id_usuario: Mapped[int] = mapped_column(BigInteger, ForeignKey("usuario.id"), nullable=False)
    lido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    usuario: Mapped["Usuario"] = relationship(back_populates="notificacoes")
