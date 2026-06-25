"""Leitura e escrita de arquivos para a cifra de 32 bits."""

from .block_cipher import decrypt_block, encrypt_block
from .keyschedule import derive_subkeys
from .padding import add_padding, remove_padding


def _bytes_to_word(chunk: bytes) -> int:
    return int.from_bytes(chunk, "big")


def _word_to_bytes(word: int) -> bytes:
    return (word & 0xFFFFFFFF).to_bytes(4, "big")


def encrypt_bytes(data: bytes, password: str) -> bytes:
    subkeys = derive_subkeys(password)
    padded = add_padding(data)
    output = bytearray()
    for offset in range(0, len(padded), 4):
        output.extend(_word_to_bytes(encrypt_block(_bytes_to_word(padded[offset:offset + 4]), subkeys)))
    return bytes(output)


def decrypt_bytes(data: bytes, password: str) -> bytes:
    if len(data) % 4 != 0:
        raise ValueError("arquivo cifrado invalido: tamanho nao e multiplo de 4")
    subkeys = derive_subkeys(password)
    output = bytearray()
    for offset in range(0, len(data), 4):
        output.extend(_word_to_bytes(decrypt_block(_bytes_to_word(data[offset:offset + 4]), subkeys)))
    return remove_padding(bytes(output))


def process_file(mode: str, password: str, input_path: str, output_path: str) -> None:
    with open(input_path, "rb") as source:
        data = source.read()
    if mode == "encrypt":
        result = encrypt_bytes(data, password)
    elif mode == "decrypt":
        result = decrypt_bytes(data, password)
    else:
        raise ValueError("modo deve ser encrypt ou decrypt")
    with open(output_path, "wb") as target:
        target.write(result)

