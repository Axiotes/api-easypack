"""Checksum de integridade calculado em paralelo via OpenCL (GPU, ou CPU quando não há GPU
disponível). Usado nos endpoints de listagem mais acessados como uma verificação extra,
sem alterar o formato das respostas (vai só num header).

Se não houver nenhum dispositivo OpenCL disponível na máquina (ex.: ambiente de produção
sem driver instalado), as funções aqui simplesmente não calculam nada — nunca derrubam
a aplicação por isso.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_KERNEL_SOURCE = """
__kernel void ponderar(__global const int *valores, __global int *saida) {
    int i = get_global_id(0);
    saida[i] = valores[i] * (i + 1);
}
"""

_indisponivel = False
_contexto = None
_fila = None
_programa = None
_kernel = None
_nome_dispositivo: str | None = None


def _escolher_dispositivo(cl):
    """Prioriza GPU NVIDIA, depois qualquer GPU, depois qualquer outro dispositivo (ex.: CPU)."""
    plataformas = cl.get_platforms()
    if not plataformas:
        raise RuntimeError("Nenhuma plataforma OpenCL encontrada")

    for plataforma in plataformas:
        if "NVIDIA" in plataforma.name.upper():
            dispositivos = plataforma.get_devices(device_type=cl.device_type.GPU)
            if dispositivos:
                return dispositivos[0]

    for plataforma in plataformas:
        dispositivos = plataforma.get_devices(device_type=cl.device_type.GPU)
        if dispositivos:
            return dispositivos[0]

    for plataforma in plataformas:
        dispositivos = plataforma.get_devices()
        if dispositivos:
            return dispositivos[0]

    raise RuntimeError("Nenhum dispositivo OpenCL encontrado")


def _preparar() -> bool:
    """Inicializa contexto/fila/programa/kernel uma única vez. Retorna False se OpenCL não estiver disponível."""
    global _indisponivel, _contexto, _fila, _programa, _kernel, _nome_dispositivo

    if _programa is not None:
        return True
    if _indisponivel:
        return False

    try:
        import pyopencl as cl

        dispositivo = _escolher_dispositivo(cl)
        _contexto = cl.Context([dispositivo])
        _fila = cl.CommandQueue(_contexto)
        _programa = cl.Program(_contexto, _KERNEL_SOURCE).build()
        _kernel = cl.Kernel(_programa, "ponderar")
        _nome_dispositivo = dispositivo.name
        logger.info("OpenCL disponível, usando dispositivo: %s", _nome_dispositivo)
        return True
    except Exception as exc:  # pragma: no cover - depende do ambiente/driver da máquina
        logger.warning("OpenCL indisponível, checksums de integridade serão omitidos: %s", exc)
        _indisponivel = True
        return False


def dispositivo_atual() -> str | None:
    """Nome do dispositivo OpenCL em uso, ou None se indisponível (sem forçar inicialização ainda)."""
    _preparar()
    return _nome_dispositivo


def checksum_gpu(valores: list[int]) -> int | None:
    """Calcula valores[i] * (i + 1) em paralelo (um work item por posição) e soma o resultado.

    Retorna None quando não há dispositivo OpenCL disponível, para o chamador decidir o
    que fazer (aqui: simplesmente omitir o header de checksum).
    """
    if not valores:
        return 0
    if not _preparar():
        return None

    import numpy as np
    import pyopencl as cl

    entrada = np.array(valores, dtype=np.int32)
    saida = np.empty_like(entrada)

    mf = cl.mem_flags
    buffer_entrada = cl.Buffer(_contexto, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=entrada)
    buffer_saida = cl.Buffer(_contexto, mf.WRITE_ONLY, saida.nbytes)

    _kernel(_fila, entrada.shape, None, buffer_entrada, buffer_saida)
    cl.enqueue_copy(_fila, saida, buffer_saida)

    return int(np.sum(saida, dtype=np.int64))
