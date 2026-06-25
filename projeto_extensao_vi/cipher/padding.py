"""Padding tipo PKCS#7 adaptado para blocos de 4 bytes."""

BLOCK_SIZE = 4


def add_padding(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    if pad_len == 0:
        pad_len = BLOCK_SIZE
    return data + bytes([pad_len]) * pad_len


def remove_padding(data: bytes) -> bytes:
    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("dados cifrados invalidos: tamanho nao e multiplo de 4")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("padding invalido")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("padding invalido")
    return data[:-pad_len]

