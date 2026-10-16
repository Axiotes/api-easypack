from app.core.constantes import (
    PRODUTO_PAGU,
    PRODUTO_PORTARIA,
    PRODUTOS_COM_ACESSO_A_PAGU,
    PRODUTOS_COM_ACESSO_A_PORTARIA,
)


def produto_atende(nm_produto_usuario: str, nm_produto_alvo: str) -> bool:
    """Verifica se um usuário do produto `nm_produto_usuario` pode atuar sobre algo do produto `nm_produto_alvo`."""
    if nm_produto_usuario == nm_produto_alvo:
        return True
    if nm_produto_alvo == PRODUTO_PAGU and nm_produto_usuario in PRODUTOS_COM_ACESSO_A_PAGU:
        return True
    if nm_produto_alvo == PRODUTO_PORTARIA and nm_produto_usuario in PRODUTOS_COM_ACESSO_A_PORTARIA:
        return True
    return False
