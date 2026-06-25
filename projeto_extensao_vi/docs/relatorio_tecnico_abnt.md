# Cifra de Blocos Simetrica Inn Seguros

Trabalho academico de extensao em Seguranca de Sistemas e Criptografia.

## Introducao

Este documento descreve uma cifra de blocos simetrica original e didatica criada para a empresa ficticia Inn Seguros. O objetivo nao e fornecer seguranca industrial, mas demonstrar conceitos de substituicao, permutacao, difusao, padding e efeito avalanche em uma implementacao verificavel.

O algoritmo processa blocos de 32 bits e usa uma chave textual de qualquer tamanho. A chave textual e reduzida para uma chave mestra de 32 bits por um procedimento manual, deterministico e implementado apenas com bytes, inteiros, XOR, deslocamentos, rotacoes e S-box propria.

## Descricao do Algoritmo

A cifra segue uma arquitetura de rede de substituicao-permutacao (SPN). Cada bloco de 32 bits e interpretado como 8 nibbles de 4 bits. A implementacao usa 6 rodadas, superando o minimo de 3 rodadas pedido no enunciado.

Em cada rodada ocorre:

1. Mistura inicial do bloco com a subchave da rodada por XOR.
2. Substituicao de cada nibble por uma S-box manual de 4 bits.
3. Key-whitening por nibble dentro da camada de substituicao.
4. Permutacao dos 32 bits por uma P-box escolhida com base em bits da subchave.

Para decriptar, o algoritmo aplica as rodadas em ordem inversa usando P-box inversa, S-box inversa e o mesmo XOR com a subchave.

## S-box

A S-box e uma permutacao manual dos 16 valores possiveis de um nibble:

`[C, 5, 6, B, 9, 0, A, D, 3, E, F, 8, 4, 7, 1, 2]`

Ela foi escolhida para evitar relacoes lineares obvias entre entradas vizinhas e saidas vizinhas. Como a tabela e uma permutacao, existe uma S-box inversa unica, usada na decriptacao.

## P-box

A camada de permutacao espalha bits entre diferentes posicoes do bloco. O codigo possui quatro tabelas P-box fixas e escolhe uma delas a cada rodada a partir de bits da subchave. Esse desenho faz a difusao depender da chave, mantendo a operacao totalmente reversivel por meio da tabela inversa correspondente.

## Derivacao de Chave

A chave textual fornecida pelo usuario e codificada em UTF-8. Cada byte e combinado em um acumulador de 32 bits por XOR em posicoes rotativas, seguido de rotacoes e aplicacao da S-box sobre todos os nibbles. Senhas vazias tambem produzem uma chave deterministica.

A partir da chave mestra, o key schedule gera 6 subchaves de 32 bits. Cada subchave usa rotacoes, XOR com constantes de rodada e uma nova passada pela S-box. Assim, cada rodada recebe uma subchave diferente.

## Padding

O padding segue um esquema do tipo PKCS#7 adaptado a blocos de 4 bytes. Se faltam N bytes para completar o bloco, sao adicionados N bytes de valor N. Quando o arquivo ja e multiplo de 4 bytes, um bloco completo `04 04 04 04` e adicionado. Isso evita ambiguidade na remocao do padding durante a decriptacao.

## Justificativa das Rodadas

O minimo solicitado era de 3 rodadas. A implementacao usa 6 rodadas para aumentar a difusao: a primeira rodada ja introduz confusao pela S-box e mistura de chave; as rodadas seguintes espalham diferencas entre nibbles e bits por meio das P-boxes dependentes da subchave. O resultado e um efeito avalanche perceptivel ja a partir da segunda rodada no exemplo testado.

## Exemplo Rodada a Rodada e Efeito Avalanche

Texto claro de 32 bits: `0x496E6E53`.

Chave A: `Q`, byte `0x51`.
Chave B: `Y`, byte `0x59`.

As chaves diferem em exatamente 1 bit, pois `0x51 XOR 0x59 = 0x08`.

| Rodada | Cifra A | Cifra B | Bits diferentes | Percentual |
|---:|---:|---:|---:|---:|
| 1 | `0xA9960297` | `0xE9406995` | 12/32 | 37.50% |
| 2 | `0x816FF7DF` | `0x7E564EA0` | 24/32 | 75.00% |
| 3 | `0x2446BBC6` | `0xDB709D08` | 20/32 | 62.50% |
| 4 | `0x068941BE` | `0x51EB2F97` | 16/32 | 50.00% |
| 5 | `0xBC640B99` | `0x8670D2C8` | 14/32 | 43.75% |
| 6 | `0xBF4B2310` | `0x703ECDA9` | 22/32 | 68.75% |

Na rodada final, 22 dos 32 bits mudaram, o que corresponde a 68.75%. Esse resultado demonstra o efeito avalanche de forma visivel.

## Testes Automatizados

A suite de testes cobre:

- derivacao de chave mestra e subchaves;
- S-box e S-box inversa para todos os 16 nibbles;
- P-box e P-box inversa para blocos e chaves de amostra;
- encriptacao e decriptacao de um unico bloco;
- padding em arquivos vazios, tamanhos pequenos e multiplos de 4;
- round-trip de bytes e arquivos reais;
- efeito avalanche com duas chaves que diferem em exatamente 1 bit.

Saida final da suite: 10 testes executados com sucesso.

## Referencias

STALLINGS, William. Cryptography and Network Security: Principles and Practice. 8. ed. Pearson, 2020.

MENEZES, Alfred J.; VAN OORSCHOT, Paul C.; VANSTONE, Scott A. Handbook of Applied Cryptography. Boca Raton: CRC Press, 1996.

NIST. Recommendation for Block Cipher Modes of Operation: Methods and Techniques. Special Publication 800-38A. Gaithersburg: National Institute of Standards and Technology, 2001.

