"""S-box manual de 4 bits e sua inversa.

A tabela abaixo e uma permutacao dos 16 valores de um nibble. Ela foi escolhida
para evitar relacoes lineares obvias: valores vizinhos de entrada nao viram
valores vizinhos de saida, e cada bit de entrada influencia mais de um bit de
saida na maior parte dos casos.
"""

SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

INV_SBOX = [0] * 16
for index, value in enumerate(SBOX):
    INV_SBOX[value] = index


def sbox(value: int) -> int:
    """Substitui um nibble por outro nibble usando a tabela manual."""
    return SBOX[value & 0xF]


def inv_sbox(value: int) -> int:
    """Desfaz a substituicao de um nibble feita por sbox()."""
    return INV_SBOX[value & 0xF]


def substitute_block(block: int, subkey: int) -> int:
    """Aplica substituicao em 8 nibbles com key-whitening por nibble.

    Cada nibble do bloco e misturado por XOR com o nibble correspondente da
    subchave antes de entrar na S-box. Esse whitening faz a camada de
    substituicao depender da subchave da rodada.
    """
    result = 0
    for pos in range(8):
        block_nibble = (block >> (pos * 4)) & 0xF
        key_nibble = (subkey >> (pos * 4)) & 0xF
        result |= sbox(block_nibble ^ key_nibble) << (pos * 4)
    return result & 0xFFFFFFFF


def inverse_substitute_block(block: int, subkey: int) -> int:
    """Desfaz substitute_block() usando a S-box inversa e o mesmo XOR."""
    result = 0
    for pos in range(8):
        cipher_nibble = (block >> (pos * 4)) & 0xF
        key_nibble = (subkey >> (pos * 4)) & 0xF
        result |= (inv_sbox(cipher_nibble) ^ key_nibble) << (pos * 4)
    return result & 0xFFFFFFFF

