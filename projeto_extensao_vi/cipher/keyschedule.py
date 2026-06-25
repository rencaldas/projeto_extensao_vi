"""Derivacao manual de chave mestra e subchaves."""

from .sbox import sbox

MASK32 = 0xFFFFFFFF
ROUNDS = 6
ROUND_CONSTANTS = [0x9E3779B9, 0x3C6EF372, 0xDAA66D2B, 0x78DDE6E4, 0x1715609D, 0xB54CDA56]


def rotl32(value: int, amount: int) -> int:
    amount &= 31
    return ((value << amount) | (value >> (32 - amount))) & MASK32


def rotr32(value: int, amount: int) -> int:
    amount &= 31
    return ((value >> amount) | (value << (32 - amount))) & MASK32


def _sbox_word(value: int) -> int:
    """Aplica a S-box em todos os nibbles de uma palavra de 32 bits."""
    result = 0
    for pos in range(8):
        result |= sbox((value >> (pos * 4)) & 0xF) << (pos * 4)
    return result & MASK32


def derive_master_key(password: str) -> int:
    """Comprime ou expande uma string para 32 bits sem usar hash de biblioteca.

    A string e convertida para UTF-8. Cada byte entra por XOR em um acumulador,
    seguido por rotacoes e uma passada parcial pela S-box. Para senha vazia,
    ainda ha uma chave deterministica nao nula.
    """
    data = password.encode("utf-8")
    key = 0xC1F4A11A
    if not data:
        data = b"\x00"
    for index, byte in enumerate(data):
        shift = (index % 4) * 8
        key ^= (byte & 0xFF) << shift
        key = rotl32(key, 5) ^ rotr32(key, 7) ^ ((index + 1) * 0x45D9F3B)
        key = _sbox_word(key)
    key ^= (len(data) & 0xFFFFFFFF) ^ rotl32(len(data), 11)
    return key & MASK32


def expand_subkeys(master_key: int, rounds: int = ROUNDS) -> list[int]:
    """Gera subchaves diferentes por rodada com rotacoes, XOR e S-box."""
    subkeys = []
    state = master_key & MASK32
    for round_index in range(rounds):
        constant = ROUND_CONSTANTS[round_index % len(ROUND_CONSTANTS)]
        state = rotl32(state ^ constant ^ round_index, (round_index * 5 + 3) % 32)
        state ^= rotr32(master_key, round_index + 1)
        state = _sbox_word(state)
        subkeys.append(state & MASK32)
    return subkeys


def derive_subkeys(password: str, rounds: int = ROUNDS) -> list[int]:
    return expand_subkeys(derive_master_key(password), rounds)

