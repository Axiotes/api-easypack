from app.models.usuario import CargoUsuario

# Ordem hierárquica dos cargos, do mais sênior para o mais júnior.
CARGO_HIERARQUIA: tuple[CargoUsuario, ...] = (
    CargoUsuario.GERENTE_PROJETO,
    CargoUsuario.COORDENADOR,
    CargoUsuario.ESPECIALISTA,
    CargoUsuario.SENIOR,
    CargoUsuario.PLENO,
    CargoUsuario.JUNIOR,
    CargoUsuario.ESTAGIARIO,
)


def cargo_rank(cargo: CargoUsuario) -> int:
    return CARGO_HIERARQUIA.index(cargo)


def cargo_pelo_menos(cargo: CargoUsuario, minimo: CargoUsuario) -> bool:
    return cargo_rank(cargo) <= cargo_rank(minimo)


def cargo_abaixo_de(cargo: CargoUsuario, referencia: CargoUsuario) -> bool:
    return cargo_rank(cargo) > cargo_rank(referencia)


# Cargos "dev" (execução técnica): podem aprovar o code review de uma correção do seu produto.
CARGOS_APROVACAO_CODE_REVIEW: tuple[CargoUsuario, ...] = (
    CargoUsuario.ESPECIALISTA,
    CargoUsuario.SENIOR,
    CargoUsuario.PLENO,
    CargoUsuario.JUNIOR,
)

# Cargos elegíveis para aprovar a aplicação de um pacote por um usuário Estagiário.
CARGOS_APROVADOR_PAR_ESTAGIARIO: tuple[CargoUsuario, ...] = (
    CargoUsuario.COORDENADOR,
    CargoUsuario.ESPECIALISTA,
    CargoUsuario.SENIOR,
    CargoUsuario.PLENO,
)
