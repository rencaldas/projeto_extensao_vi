# Relatorio de efeito avalanche

Texto claro de 32 bits: `0x496E6E53`.
Chave A: `Q` -> mestre `0xF79F0AC4`.
Chave B: `Y` -> mestre `0x879F09C4`.
As chaves textuais diferem em exatamente 1 bit: `0x51 XOR 0x59 = 0x08`.

| Rodada | Cifra A | Cifra B | Bits diferentes | Percentual |
|---:|---:|---:|---:|---:|
| 1 | `0xA9960297` | `0xE9406995` | 12/32 | 37.50% |
| 2 | `0x816FF7DF` | `0x7E564EA0` | 24/32 | 75.00% |
| 3 | `0x2446BBC6` | `0xDB709D08` | 20/32 | 62.50% |
| 4 | `0x068941BE` | `0x51EB2F97` | 16/32 | 50.00% |
| 5 | `0xBC640B99` | `0x8670D2C8` | 14/32 | 43.75% |
| 6 | `0xBF4B2310` | `0x703ECDA9` | 22/32 | 68.75% |

Resultado final: 22 de 32 bits mudaram (68.75%).

Observacao: a comparacao altera exatamente 1 bit da chave textual e mede a divergencia rodada a rodada.
