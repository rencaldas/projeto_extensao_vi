"""Gera demonstracao de efeito avalanche e salva docs/avalanche_report.md."""

from pathlib import Path

from cipher.block_cipher import trace_encrypt_block
from cipher.keyschedule import ROUNDS, derive_master_key


def bit_count(value: int) -> int:
    return bin(value & 0xFFFFFFFF).count("1")


def make_report() -> str:
    plaintext = 0x496E6E53  # ASCII: InnS
    key_a = "Q"  # 0x51
    key_b = "Y"  # 0x59: difere de Q em exatamente 1 bit

    trace_a = trace_encrypt_block(plaintext, key_a, ROUNDS)
    trace_b = trace_encrypt_block(plaintext, key_b, ROUNDS)

    lines = [
        "# Relatorio de efeito avalanche",
        "",
        "Texto claro de 32 bits: `0x%08X`." % plaintext,
        "Chave A: `%s` -> mestre `0x%08X`." % (key_a, derive_master_key(key_a)),
        "Chave B: `%s` -> mestre `0x%08X`." % (key_b, derive_master_key(key_b)),
        "As chaves textuais diferem em exatamente 1 bit: `0x51 XOR 0x59 = 0x08`.",
        "",
        "| Rodada | Cifra A | Cifra B | Bits diferentes | Percentual |",
        "|---:|---:|---:|---:|---:|",
    ]
    total = 0
    for index, (left, right) in enumerate(zip(trace_a, trace_b), start=1):
        changed = bit_count(left ^ right)
        total = changed
        lines.append("| %d | `0x%08X` | `0x%08X` | %d/32 | %.2f%% |" % (
            index, left, right, changed, (changed / 32) * 100
        ))
    lines.extend([
        "",
        "Resultado final: %d de 32 bits mudaram (%.2f%%)." % (total, (total / 32) * 100),
        "",
        "Observacao: a comparacao altera exatamente 1 bit da chave textual e mede a divergencia rodada a rodada.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    report = make_report()
    path = Path("docs") / "avalanche_report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
