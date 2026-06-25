"""CLI da cifra da Inn Seguros."""

import argparse
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from cipher.file_io import process_file
else:
    from .file_io import process_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cifra de blocos didatica da Inn Seguros")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="modo de operacao")
    parser.add_argument("key", help="chave textual de qualquer tamanho")
    parser.add_argument("input", help="arquivo de entrada")
    parser.add_argument("output", help="arquivo de saida")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    process_file(args.mode, args.key, args.input, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
