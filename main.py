"""
==========================================================
 SIMULADOR DE SOBREVIVÊNCIA
==========================================================
Projeto acadêmico desenvolvido em Python puro (sem
dependências externas), utilizando:
    - Listas aninhadas (inventário, sobreviventes)
    - Matrizes (mapa de exploração)
    - Funções bem definidas (uma para cada responsabilidade)
    - Manipulação de strings (formatação de menus, nomes,
      relatórios e parsing de entradas do usuário)

Como executar:
    python3 main.py
==========================================================
"""

import random

# ----------------------------------------------------------------------
# CONSTANTES GLOBAIS
# ----------------------------------------------------------------------

RECURSOS_POSSIVEIS = ["Madeira", "Pedra", "Água", "Comida", "Metal"]
TAMANHO_MAPA = 5  # matriz 5x5

# Receitas de construção: cada item precisa de uma lista de recursos
# no formato [nome_recurso, quantidade_necessaria]
RECEITAS = {
    "Machado":               [["Madeira", 3], ["Pedra", 2]],
    "Fogueira":               [["Madeira", 5], ["Pedra", 3]],
    "Abrigo":                 [["Madeira", 10], ["Pedra", 5]],
    "Lança":                  [["Madeira", 2], ["Metal", 1]],
    "Purificador de Água":    [["Metal", 4], ["Pedra", 2]],
}

EVENTOS = [
    "chuva_forte",
    "animal_selvagem",
    "bau_escondido",
    "sobrevivente_perdido",
    "tempestade_de_areia",
]


# ----------------------------------------------------------------------
# FUNÇÕES DE APOIO / STRINGS
# ----------------------------------------------------------------------

def formatar_titulo(texto):
    """Recebe um texto e devolve um cabeçalho formatado (manipulação de strings)."""
    linha = "-" * (len(texto) + 4)
    return f"\n{linha}\n| {texto.upper()} |\n{linha}"


def normalizar_nome(nome):
    """Remove espaços extras e deixa a primeira letra de cada palavra maiúscula."""
    return nome.strip().title()


def pausar():
    input("\nPressione ENTER para continuar...")


# ----------------------------------------------------------------------
# 1. CADASTRO DE SOBREVIVENTES
# ----------------------------------------------------------------------
# Estrutura: lista de dicionários (lista aninhada)
# sobreviventes = [
#     {"nome": "Ana", "vida": 100, "fome": 100, "sede": 100},
#     ...
# ]

def cadastrar_sobrevivente(sobreviventes):
    print(formatar_titulo("Cadastro de Sobrevivente"))
    nome_bruto = input("Nome do sobrevivente: ")
    nome = normalizar_nome(nome_bruto)

    if nome == "":
        print("Nome inválido. Cadastro cancelado.")
        return

    for s in sobreviventes:
        if s["nome"].lower() == nome.lower():
            print(f"Já existe um sobrevivente chamado '{nome}'.")
            return

    novo = {"nome": nome, "vida": 100, "fome": 100, "sede": 100}
    sobreviventes.append(novo)
    print(f"Sobrevivente '{nome}' cadastrado com sucesso!")


def listar_sobreviventes(sobreviventes):
    print(formatar_titulo("Sobreviventes do Acampamento"))
    if not sobreviventes:
        print("Nenhum sobrevivente cadastrado ainda.")
        return

    for i, s in enumerate(sobreviventes, start=1):
        status = "OK" if s["vida"] > 0 else "MORTO"
        print(f"{i:02d}. {s['nome']:<15} | Vida: {s['vida']:>3} | "
              f"Fome: {s['fome']:>3} | Sede: {s['sede']:>3} | {status}")


def escolher_sobrevivente(sobreviventes):
    """Pede ao usuário para escolher um sobrevivente vivo e devolve o dicionário dele."""
    vivos = [s for s in sobreviventes if s["vida"] > 0]
    if not vivos:
        print("Não há sobreviventes vivos!")
        return None

    listar_sobreviventes(sobreviventes)
    nome_bruto = input("Digite o nome do sobrevivente: ")
    nome = normalizar_nome(nome_bruto)

    for s in vivos:
        if s["nome"].lower() == nome.lower():
            return s

    print("Sobrevivente não encontrado ou está morto.")
    return None


# ----------------------------------------------------------------------
# 2. MAPA DE EXPLORAÇÃO (MATRIZ) E COLETA DE RECURSOS
# ----------------------------------------------------------------------

def gerar_mapa(tamanho):
    """Gera uma matriz (lista de listas) representando a área de exploração."""
    mapa = []
    for _linha in range(tamanho):
        linha_atual = []
        for _coluna in range(tamanho):
            # 25% de chance da célula estar vazia (já explorada)
            if random.random() < 0.25:
                linha_atual.append("Vazio")
            else:
                linha_atual.append(random.choice(RECURSOS_POSSIVEIS))
        mapa.append(linha_atual)
    return mapa


def exibir_mapa(mapa):
    print(formatar_titulo("Mapa de Exploração"))
    print("     " + "  ".join(f"C{c}" for c in range(len(mapa[0]))))
    for i, linha in enumerate(mapa):
        celulas = "  ".join(f"{item[:4]:<4}" for item in linha)
        print(f"L{i}   {celulas}")


def coletar_recurso(mapa, inventario, sobrevivente):
    exibir_mapa(mapa)

    if sobrevivente["fome"] <= 0 or sobrevivente["sede"] <= 0:
        print(f"{sobrevivente['nome']} está fraco demais (fome/sede) para explorar!")
        return

    try:
        linha = int(input(f"Linha (0-{len(mapa) - 1}): "))
        coluna = int(input(f"Coluna (0-{len(mapa[0]) - 1}): "))
    except ValueError:
        print("Coordenadas inválidas.")
        return

    if not (0 <= linha < len(mapa) and 0 <= coluna < len(mapa[0])):
        print("Coordenadas fora do mapa.")
        return

    recurso = mapa[linha][coluna]

    if recurso == "Vazio":
        print("Esta célula já foi explorada e não possui recursos.")
        return

    quantidade = random.randint(1, 5)
    adicionar_ao_inventario(inventario, recurso, quantidade)
    mapa[linha][coluna] = "Vazio"

    # explorar custa fome/sede do sobrevivente
    sobrevivente["fome"] = max(0, sobrevivente["fome"] - 5)
    sobrevivente["sede"] = max(0, sobrevivente["sede"] - 5)

    print(f"{sobrevivente['nome']} coletou {quantidade}x {recurso}!")


# ----------------------------------------------------------------------
# 3. CONTROLE DE INVENTÁRIO
# ----------------------------------------------------------------------
# Estrutura: lista aninhada -> inventario = [[nome, quantidade], ...]

def adicionar_ao_inventario(inventario, nome_recurso, quantidade):
    for item in inventario:
        if item[0] == nome_recurso:
            item[1] += quantidade
            return
    inventario.append([nome_recurso, quantidade])


def remover_do_inventario(inventario, nome_recurso, quantidade):
    for item in inventario:
        if item[0] == nome_recurso:
            if item[1] >= quantidade:
                item[1] -= quantidade
                return True
            return False
    return False


def possui_recursos_suficientes(inventario, requisitos):
    """requisitos é uma lista aninhada [[recurso, quantidade], ...]"""
    for recurso, quantidade in requisitos:
        encontrado = False
        for item in inventario:
            if item[0] == recurso and item[1] >= quantidade:
                encontrado = True
                break
        if not encontrado:
            return False
    return True


def exibir_inventario(inventario):
    print(formatar_titulo("Inventário do Acampamento"))
    if not inventario:
        print("Inventário vazio.")
        return
    for item in inventario:
        nome, quantidade = item
        print(f" - {nome:<10}: {quantidade}")


# ----------------------------------------------------------------------
# 4. CONSTRUÇÃO DE ITENS
# ----------------------------------------------------------------------

def exibir_receitas():
    print(formatar_titulo("Receitas Disponíveis"))
    for nome_item, requisitos in RECEITAS.items():
        ingredientes = ", ".join(f"{q}x {r}" for r, q in requisitos)
        print(f" - {nome_item:<20}: {ingredientes}")


def construir_item(inventario, itens_construidos):
    exibir_receitas()
    nome_bruto = input("O que deseja construir? ")
    nome_item = normalizar_nome(nome_bruto)

    if nome_item not in RECEITAS:
        print("Item não encontrado na lista de receitas.")
        return

    requisitos = RECEITAS[nome_item]

    if not possui_recursos_suficientes(inventario, requisitos):
        print(f"Recursos insuficientes para construir '{nome_item}'.")
        return

    for recurso, quantidade in requisitos:
        remover_do_inventario(inventario, recurso, quantidade)

    itens_construidos.append(nome_item)
    print(f"'{nome_item}' construído com sucesso!")


def exibir_itens_construidos(itens_construidos):
    print(formatar_titulo("Itens Construídos"))
    if not itens_construidos:
        print("Nenhum item construído ainda.")
        return
    for i, item in enumerate(itens_construidos, start=1):
        print(f"{i:02d}. {item}")


# ----------------------------------------------------------------------
# 5. EVENTOS ALEATÓRIOS
# ----------------------------------------------------------------------

def evento_chuva_forte(sobreviventes, inventario):
    for s in sobreviventes:
        if s["vida"] > 0:
            s["sede"] = min(100, s["sede"] + 20)
    return "Choveu forte! A sede de todos os sobreviventes foi recuperada em 20 pontos."


def evento_animal_selvagem(sobreviventes, inventario):
    vivos = [s for s in sobreviventes if s["vida"] > 0]
    if not vivos:
        return "Um animal selvagem rondou o acampamento, mas não havia ninguém por perto."
    alvo = random.choice(vivos)
    dano = random.randint(10, 25)
    alvo["vida"] = max(0, alvo["vida"] - dano)
    return f"Um animal selvagem atacou {alvo['nome']}! Perdeu {dano} pontos de vida."


def evento_bau_escondido(sobreviventes, inventario):
    recurso = random.choice(RECURSOS_POSSIVEIS)
    quantidade = random.randint(3, 10)
    adicionar_ao_inventario(inventario, recurso, quantidade)
    return f"Um baú escondido foi encontrado! Ganhou {quantidade}x {recurso}."


def evento_sobrevivente_perdido(sobreviventes, inventario):
    nomes_possiveis = ["Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gabriela"]
    nome = random.choice(nomes_possiveis)
    for s in sobreviventes:
        if s["nome"] == nome:
            return f"{nome} apareceu, mas já fazia parte do acampamento."
    sobreviventes.append({"nome": nome, "vida": 100, "fome": 80, "sede": 80})
    return f"Um sobrevivente perdido chamado {nome} se juntou ao acampamento!"


def evento_tempestade_de_areia(sobreviventes, inventario):
    if inventario:
        item = random.choice(inventario)
        perda = min(item[1], random.randint(1, 4))
        item[1] -= perda
        return f"Tempestade de areia! Perdeu {perda}x {item[0]} do inventário."
    return "Uma tempestade de areia passou, mas o inventário já estava vazio."


MAPA_DE_EVENTOS = {
    "chuva_forte": evento_chuva_forte,
    "animal_selvagem": evento_animal_selvagem,
    "bau_escondido": evento_bau_escondido,
    "sobrevivente_perdido": evento_sobrevivente_perdido,
    "tempestade_de_areia": evento_tempestade_de_areia,
}


def disparar_evento_aleatorio(sobreviventes, inventario):
    print(formatar_titulo("Evento Aleatório"))
    nome_evento = random.choice(EVENTOS)
    funcao_evento = MAPA_DE_EVENTOS[nome_evento]
    mensagem = funcao_evento(sobreviventes, inventario)
    print(mensagem)


def passar_o_tempo(sobreviventes):
    """Reduz fome e sede a cada rodada; se chegarem a 0, a vida também cai."""
    for s in sobreviventes:
        if s["vida"] <= 0:
            continue
        s["fome"] = max(0, s["fome"] - 3)
        s["sede"] = max(0, s["sede"] - 4)
        if s["fome"] == 0 or s["sede"] == 0:
            s["vida"] = max(0, s["vida"] - 10)
            print(f"{s['nome']} está sofrendo com fome/sede e perdeu vida!")


# ----------------------------------------------------------------------
# MENU PRINCIPAL
# ----------------------------------------------------------------------

def exibir_menu():
    print(formatar_titulo("Simulador de Sobrevivência"))
    print("1 - Cadastrar sobrevivente")
    print("2 - Listar sobreviventes")
    print("3 - Explorar / Coletar recursos")
    print("4 - Ver inventário")
    print("5 - Construir item")
    print("6 - Ver itens construídos")
    print("7 - Avançar o tempo (novo dia + evento aleatório)")
    print("0 - Sair")


def main():
    sobreviventes = []
    inventario = []
    itens_construidos = []
    mapa = gerar_mapa(TAMANHO_MAPA)

    print(formatar_titulo("Bem-vindo ao Simulador de Sobrevivência"))

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_sobrevivente(sobreviventes)

        elif opcao == "2":
            listar_sobreviventes(sobreviventes)

        elif opcao == "3":
            sobrevivente = escolher_sobrevivente(sobreviventes)
            if sobrevivente:
                coletar_recurso(mapa, inventario, sobrevivente)

        elif opcao == "4":
            exibir_inventario(inventario)

        elif opcao == "5":
            construir_item(inventario, itens_construidos)

        elif opcao == "6":
            exibir_itens_construidos(itens_construidos)

        elif opcao == "7":
            passar_o_tempo(sobreviventes)
            disparar_evento_aleatorio(sobreviventes, inventario)

        elif opcao == "0":
            print("Encerrando o simulador. Até a próxima!")
            break

        else:
            print("Opção inválida, tente novamente.")

        pausar()


if __name__ == "__main__":
    main()
