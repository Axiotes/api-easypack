from __future__ import annotations

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Setor(Base):
    __tablename__ = "setor"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    nm_setor: Mapped[str] = mapped_column(String(255), nullable=False)
    sg_setor: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    subsetores: Mapped[list["Subsetor"]] = relationship(back_populates="setor")
    clientes: Mapped[list["Cliente"]] = relationship(back_populates="setor_atendimento")
    correcoes: Mapped[list["Correcao"]] = relationship(back_populates="setor")
