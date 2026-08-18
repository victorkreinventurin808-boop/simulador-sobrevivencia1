# 🏕️ Simulador de Sobrevivência

Simulador de sobrevivência em modo texto, feito **100% em Python puro**
(nenhuma biblioteca externa é necessária).

## Funcionalidades

- 👤 **Cadastro de sobreviventes** — nome, vida, fome e sede.
- 🌲 **Coleta de recursos** — explore um mapa (matriz 5x5) e colete madeira,
  pedra, água, comida e metal.
- 🔨 **Construção de itens** — combine recursos do inventário para construir
  machado, fogueira, abrigo, lança e purificador de água.
- 🎒 **Controle de inventário** — visualize e gerencie tudo o que foi
  coletado ou gasto.
- 🎲 **Eventos aleatórios** — chuva forte, ataque de animal selvagem, baú
  escondido, sobrevivente perdido e tempestade de areia.

## Requisitos

- Python 3.8 ou superior (nenhuma dependência externa / nenhum `pip install`
  necessário).

## Como executar

```bash
python3 main.py
```

O programa é 100% orientado por menu no terminal. Basta seguir as instruções
exibidas na tela.

## Estrutura do projeto

```
simulador-sobrevivencia/
├── main.py         # código-fonte completo do simulador
├── README.md        # este arquivo
└── RELATORIO.md      # relatório técnico explicando a lógica utilizada
```

## Estruturas de dados utilizadas

| Conceito exigido      | Onde é usado                                                   |
|------------------------|-----------------------------------------------------------------|
| Listas aninhadas       | Inventário (`[[nome, quantidade], ...]`) e lista de sobreviventes (lista de dicionários) |
| Matrizes (listas 2D)   | Mapa de exploração 5x5 (`mapa[linha][coluna]`)                  |
| Funções bem definidas  | Cada funcionalidade possui sua própria função (cadastro, coleta, construção, inventário, eventos) |
| Manipulação de strings | Formatação de menus, normalização de nomes (`.title()`, `.strip()`), montagem de mensagens de eventos |

## Autor

Projeto acadêmico — Simulador de Sobrevivência em Python.
