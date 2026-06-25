"""Cifra de blocos SPN de 32 bits da Inn Seguros."""

from .keyschedule import ROUNDS, derive_subkeys
from .pbox import inverse_permute_block, permute_block
from .sbox import inverse_substitute_block, substitute_block

MASK32 = 0xFFFFFFFF


def encrypt_round(block: int, subkey: int) -> int:
    """Uma rodada: substituicao dependente de chave seguida de permutacao."""
    block = substitute_block(block ^ subkey, subkey)
    return permute_block(block, subkey)


def decrypt_round(block: int, subkey: int) -> int:
    """Desfaz uma rodada aplicando P-box inversa e S-box inversa."""
    block = inverse_permute_block(block, subkey)
    block = inverse_substitute_block(block, subkey)
    return (block ^ subkey) & MASK32


def encrypt_block(block: int, subkeys: list[int]) -> int:
    """Encripta uma palavra de 32 bits usando todas as subchaves."""
    value = block & MASK32
    for subkey in subkeys:
        value = encrypt_round(value, subkey)
    return value & MASK32


def decrypt_block(block: int, subkeys: list[int]) -> int:
    """Decripta uma palavra de 32 bits aplicando as rodadas ao contrario."""
    value = block & MASK32
    for subkey in reversed(subkeys):
        value = decrypt_round(value, subkey)
    return value & MASK32


def trace_encrypt_block(block: int, password: str, rounds: int = ROUNDS) -> list[int]:
    """Retorna o estado cifrado apos cada rodada para demonstrar avalanche."""
    subkeys = derive_subkeys(password, rounds)
    value = block & MASK32
    trace = []
    for subkey in subkeys:
        value = encrypt_round(value, subkey)
        trace.append(value)
    return trace

