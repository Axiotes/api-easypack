from __future__ import annotations

import enum

from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class CargoUsuario(str, enum.Enum):
    GERENTE_PROJETO = "GERENTE_PROJETO"
    COORDENADOR = "COORDENADOR"
    ESPECIALISTA = "ESPECIALISTA"
    SENIOR = "SENIOR"
    PLENO = "PLENO"
    JUNIOR = "JUNIOR"
    ESTAGIARIO = "ESTAGIARIO"


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    nm_usuario: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    id_subsetor: Mapped[int] = mapped_column(BigInteger, ForeignKey("subsetor.id"), nullable=False)
    cargo: Mapped[CargoUsuario] = mapped_column(SAEnum(CargoUsuario, name="cargo_usuario"), nullable=False)
    id_produto: Mapped[int] = mapped_column(BigInteger, ForeignKey("produto.id"), nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    nm_completo: Mapped[str] = mapped_column(String(255), nullable=False)

    subsetor: Mapped["Subsetor"] = relationship(back_populates="usuarios")
    produto: Mapped["Produto"] = relationship(back_populates="usuarios")
    clientes: Mapped[list["Cliente"]] = relationship(back_populates="usuario")
    correcoes: Mapped[list["Correcao"]] = relationship(
        back_populates="usuario", foreign_keys="[Correcao.id_usuario]"
    )
