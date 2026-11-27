from __future__ import annotations

from sqlalchemy import BigInteger, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    nm_cliente: Mapped[str] = mapped_column(String(255), nullable=False)
    estado: Mapped[str | None] = mapped_column(String(2), nullable=True)
    status_ambiente: Mapped[str] = mapped_column(
        Enum("PRE-PROD", "PRD", name="status_ambiente_cliente", create_constraint=True, validate_strings=True),
        nullable=False,
        server_default="PRE-PROD",
    )
    id_setor_atendimento: Mapped[int] = mapped_column(BigInteger, ForeignKey("setor.id"), nullable=False)
    id_usuario: Mapped[int] = mapped_column(BigInteger, ForeignKey("usuario.id"), nullable=False)

    setor_atendimento: Mapped["Setor"] = relationship(back_populates="clientes")
    usuario: Mapped["Usuario"] = relationship(back_populates="clientes")
    correcoes: Mapped[list["Correcao"]] = relationship(back_populates="cliente")
