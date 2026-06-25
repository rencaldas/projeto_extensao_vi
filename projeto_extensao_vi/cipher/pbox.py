"""Permutacao de bits dependente da subchave."""

PBOXES = [
    [0, 8, 16, 24, 1, 9, 17, 25, 2, 10, 18, 26, 3, 11, 19, 27,
     4, 12, 20, 28, 5, 13, 21, 29, 6, 14, 22, 30, 7, 15, 23, 31],
    [31, 23, 15, 7, 30, 22, 14, 6, 29, 21, 13, 5, 28, 20, 12, 4,
     27, 19, 11, 3, 26, 18, 10, 2, 25, 17, 9, 1, 24, 16, 8, 0],
    [0, 5, 10, 15, 20, 25, 30, 3, 8, 13, 18, 23, 28, 1, 6, 11,
     16, 21, 26, 31, 4, 9, 14, 19, 24, 29, 2, 7, 12, 17, 22, 27],
    [2, 11, 20, 29, 6, 15, 24, 1, 10, 19, 28, 5, 14, 23, 0, 9,
     18, 27, 4, 13, 22, 31, 8, 17, 26, 3, 12, 21, 30, 7, 16, 25],
]


def _inverse_table(table: list[int]) -> list[int]:
    inverse = [0] * 32
    for source, target in enumerate(table):
        inverse[target] = source
    return inverse


INV_PBOXES = [_inverse_table(table) for table in PBOXES]


def _select_table(subkey: int) -> int:
    """Escolhe uma P-box fixa usando bits da subchave da rodada."""
    return ((subkey >> 29) ^ (subkey >> 13) ^ subkey) & 0x3


def permute_block(block: int, subkey: int) -> int:
    """Espalha bits do bloco de acordo com uma tabela escolhida pela subchave."""
    table = PBOXES[_select_table(subkey)]
    result = 0
    for source in range(32):
        bit = (block >> source) & 1
        result |= bit << table[source]
    return result & 0xFFFFFFFF


def inverse_permute_block(block: int, subkey: int) -> int:
    """Desfaz permute_block() usando a tabela inversa correspondente."""
    table = INV_PBOXES[_select_table(subkey)]
    result = 0
    for source in range(32):
        bit = (block >> source) & 1
        result |= bit << table[source]
    return result & 0xFFFFFFFF

