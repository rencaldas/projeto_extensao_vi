# Cifra de Blocos da Inn Seguros

Projeto acadêmico de uma cifra de blocos simétrica original (rede de substituição-permutação), implementada em **Python 3 puro**, sem nenhuma dependência externa de compilação ou execução e sem uso de facilidades de criptografia da linguagem (nada de `hashlib`, `secrets`, `hmac` etc.).

## Sobre o projeto

Cenário do trabalho: a seguradora fictícia **Inn Seguros**, preocupada com violações de dados, contrata uma equipe de segurança da informação para projetar e implementar, do zero, um algoritmo próprio de cifra de blocos capaz de proteger contratos, sinistros e dados pessoais de clientes.

Este repositório contém a implementação completa do algoritmo, sua suíte de testes e a demonstração do efeito avalanche pedidos pelo trabalho de extensão.

## Características

- Cifra de blocos simétrica, rede de substituição-permutação (SPN)
- Bloco de **32 bits**, chave de **32 bits** derivada de uma string fornecida pelo usuário
- No mínimo **3 rodadas**, cada uma com sua própria subchave (key schedule próprio)
- Substituição (S-box) e permutação (P-box) **dependentes de chave**
- Padding próprio, suporta arquivos de qualquer tamanho (não precisa ser múltiplo de 4 bytes)
- 100% biblioteca padrão do Python — sem `pip install`, sem bibliotecas de criptografia
- Suíte de testes automatizados (round-trip, S-box/P-box inversas, casos de borda)
- Demonstração quantitativa do efeito avalanche, com relatório gerado automaticamente

## ⚠️ Aviso importante

Este é um **projeto acadêmico e didático**. O algoritmo aqui implementado não passou por nenhuma análise criptográfica formal, não foi revisado por especialistas e **não deve ser usado para proteger dados reais**. O objetivo é estudar na prática os conceitos de substituição, permutação, difusão e efeito avalanche — não produzir uma cifra segura para produção.

## Estrutura do projeto

```
.
├── cipher/
│   ├── cli.py            # interface de linha de comando (encrypt/decrypt)
│   ├── keyschedule.py    # deriva a chave mestra e as subchaves de cada rodada
│   ├── sbox.py           # substituição (S-box de 4 bits) e sua inversa
│   ├── pbox.py           # permutação dependente de chave e sua inversa
│   ├── block_cipher.py   # função de rodada, encrypt_block / decrypt_block
│   ├── padding.py        # aplica e remove o padding dos arquivos
│   └── file_io.py        # leitura/escrita dos arquivos em blocos de 4 bytes
├── tests/
│   ├── test_roundtrip.py # decrypt(encrypt(x)) == x, vários arquivos e chaves
│   ├── test_padding.py   # casos de borda (arquivo vazio, múltiplo de 4, etc.)
│   └── test_sbox_pbox.py # garante que as inversas desfazem corretamente
├── docs/
│   └── avalanche_report.md   # gerado automaticamente por avalanche_demo.py
├── avalanche_demo.py
└── README.md
```

> Os nomes acima seguem a arquitetura planejada para o projeto. Se algum arquivo do seu repositório tiver nome diferente, ajuste esta árvore antes de publicar.

## Requisitos

- Python 3.8 ou superior
- Nenhuma instalação adicional — usa apenas a biblioteca padrão

## Uso

### Encriptar um arquivo

```bash
python cipher/cli.py encrypt "minha chave" entrada.bin saida.cif
```

### Decriptar um arquivo

```bash
python cipher/cli.py decrypt "minha chave" saida.cif restaurado.bin
```

| Argumento | Descrição                                       |
|-----------|--------------------------------------------------|
| modo      | `encrypt` ou `decrypt`                           |
| chave     | string usada para derivar a chave de 32 bits     |
| entrada   | caminho do arquivo de entrada                    |
| saída     | caminho do arquivo de saída a ser gerado         |

## Como o algoritmo funciona (resumo)

1. **Derivação de chave** — a string fornecida pelo usuário é reduzida/expandida para uma chave mestra de 32 bits; a partir dela, uma função de expansão própria deriva uma subchave de 32 bits diferente para cada rodada.
2. **Substituição** — o bloco de 32 bits é dividido em 8 nibbles (4 bits cada); cada nibble passa por XOR com a subchave da rodada e, em seguida, por uma S-box de 4 bits.
3. **Permutação** — os bits resultantes passam por uma permutação dependente da subchave da rodada.
4. **Rodadas** — os passos 2 e 3 se repetem por, no mínimo, 3 rodadas, cada uma com subchave própria.
5. **Decriptação** — aplica as rodadas na ordem inversa, usando a S-box e a P-box inversas.
6. **Padding** — arquivos cujo tamanho não é múltiplo de 4 bytes recebem um padding (esquema tipo PKCS#7 adaptado a blocos de 4 bytes), removido automaticamente na decriptação.

A justificativa detalhada de cada escolha de design (quantidade de rodadas, critério de não-linearidade da S-box, tratamento do alinhamento do texto claro, etc.) está no documento técnico em PDF entregue junto com o trabalho.

## Testes

```bash
python -m unittest discover -s tests
```

Cobertura dos testes:
- **Round-trip**: `decrypt(encrypt(x, chave), chave) == x` para diversos arquivos e chaves, incluindo arquivos de tamanho não múltiplo de 4 bytes.
- **S-box / P-box**: garante que as funções inversas desfazem exatamente a substituição e a permutação.
- **Padding**: casos de borda — arquivo vazio, tamanho exatamente múltiplo de 4, tamanho não múltiplo de 4.

## Efeito avalanche

```bash
python avalanche_demo.py
```

O script encripta o mesmo texto claro com duas chaves que diferem em apenas **1 bit**, mede a porcentagem de bits do texto cifrado que mudaram a cada rodada (idealmente próxima de 50%) e salva o relatório em `docs/avalanche_report.md`.

## Contexto acadêmico

Projeto de extensão da disciplina **Segurança de Sistemas e Criptografia** — Universidade Veiga de Almeida (UVA). A entrega completa do trabalho inclui, além deste código-fonte, um documento técnico em PDF (normas ABNT) com a descrição detalhada do algoritmo, exemplos cifrados rodada a rodada e as referências bibliográficas utilizadas.

## Autoria

- [Nome completo] – [matrícula]
- [Nome completo] – [matrícula]

> Mesmo em trabalhos desenvolvidos em grupo, a entrega no Canvas é obrigatoriamente individual — confira o formato exigido na guia de entrega da disciplina.

## Licença

Projeto acadêmico, sem licença de uso comercial definida. Uso livre para fins educacionais.
