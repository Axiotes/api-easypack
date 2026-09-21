from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.usuario import Usuario


def get_by_id(db: Session, usuario_id: int) -> Usuario | None:
    return db.get(Usuario, usuario_id)


def get_by_nm_usuario(db: Session, nm_usuario: str) -> Usuario | None:
    stmt = select(Usuario).where(Usuario.nm_usuario == nm_usuario)
    return db.scalars(stmt).first()


def list_all(db: Session) -> list[Usuario]:
    return list(db.scalars(select(Usuario)).all())


def create(db: Session, usuario: Usuario) -> Usuario:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def update(db: Session, usuario: Usuario) -> Usuario:
    db.commit()
    db.refresh(usuario)
    return usuario


def delete(db: Session, usuario: Usuario) -> None:
    db.delete(usuario)
    db.commit()
