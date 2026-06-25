# Cifra de Blocos da Inn Seguros

Projeto academico em Python 3 puro, sem dependencias externas de compilacao ou execucao.

## Uso

```bash
python cipher/cli.py encrypt "minha chave" entrada.bin saida.cif
python cipher/cli.py decrypt "minha chave" saida.cif restaurado.bin
```

## Testes

```bash
python -m unittest discover -s tests
```

## Avalanche

```bash
python avalanche_demo.py
```

O script gera `docs/avalanche_report.md`.
