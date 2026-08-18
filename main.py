import random

RECURSOS_POSSIVEIS = ["Madeira", "Pedra", "Água", "Comida", "Metal"]
TAMANHO_MAPA = 5

RECEITAS = {
    "Machado": [["Madeira", 3], ["Pedra", 2]],
    "Fogueira": [["Madeira", 5], ["Pedra", 3]],
    "Abrigo": [["Madeira", 10], ["Pedra", 5]],
    "Lança": [["Madeira", 2], ["Metal", 1]],
    "Purificador de Água": [["Metal", 4], ["Pedra", 2]],
}


def formatar_titulo(texto):
    linha = "-" * (len(texto) + 4)
    return f"\n{linha}\n| {texto.upper()} |\n{linha}"


def normalizar_nome(nome):
    return nome.strip().title()


def cadastrar_sobrevivente(sobreviventes):
    print(formatar_titulo("Cadastro de Sobrevivente"))
    nome = normalizar_nome(input("Nome do sobrevivente: "))

    if nome == "":
        print("Nome inválido.")
        return

    for s in sobreviventes:
        if s["nome"].lower() == nome.lower():
            print(f"Já existe um sobrevivente chamado '{nome}'.")
            return

    sobreviventes.append({"nome": nome, "vida": 100, "fome": 100, "sede": 100})
    print(f"Sobrevivente '{nome}' cadastrado com sucesso!")


def listar_sobreviventes(sobreviventes):
    print(formatar_titulo("Sobreviventes do Acampamento"))
    if not sobreviventes:
        print("Nenhum sobrevivente cadastrado.")
        return
    for i, s in enumerate(sobreviventes, start=1):
        status = "OK" if s["vida"] > 0 else "MORTO"
        print(f"{i:02d}. {s['nome']:<15} | Vida: {s['vida']:>3} | Fome: {s['fome']:>3} | Sede: {s['sede']:>3} | {status}")


def escolher_sobrevivente(sobreviventes):
    vivos = [s for s in sobreviventes if s["vida"] > 0]
    if not vivos:
        print("Não há sobreviventes vivos!")
        return None

    listar_sobreviventes(sobreviventes)
    nome = normalizar_nome(input("Digite o nome do sobrevivente: "))

    for s in vivos:
        if s["nome"].lower() == nome.lower():
            return s

    print("Sobrevivente não encontrado.")
    return None


def gerar_mapa(tamanho):
    mapa = []
    for _linha in range(tamanho):
        linha_atual = []
        for _coluna in range(tamanho):
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
        print(f"{sobrevivente['nome']} está fraco demais para explorar!")
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
        print("Esta célula já foi explorada.")
        return

    quantidade = random.randint(1, 5)
    adicionar_ao_inventario(inventario, recurso, quantidade)
    mapa[linha][coluna] = "Vazio"

    sobrevivente["fome"] = max(0, sobrevivente["fome"] - 5)
    sobrevivente["sede"] = max(0, sobrevivente["sede"] - 5)

    print(f"{sobrevivente['nome']} coletou {quantidade}x {recurso}!")


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
    for nome, quantidade in inventario:
        print(f" - {nome:<10}: {quantidade}")


def exibir_receitas():
    print(formatar_titulo("Receitas Disponíveis"))
    for nome_item, requisitos in RECEITAS.items():
        ingredientes = ", ".join(f"{q}x {r}" for r, q in requisitos)
        print(f" - {nome_item:<20}: {ingredientes}")


def construir_item(inventario, itens_construidos):
    exibir_receitas()
    nome_item = normalizar_nome(input("O que deseja construir? "))

    if nome_item not in RECEITAS:
        print("Item não encontrado.")
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


def evento_chuva_forte(sobreviventes, inventario):
    for s in sobreviventes:
        if s["vida"] > 0:
            s["sede"] = min(100, s["sede"] + 20)
    return "Choveu forte! A sede de todos foi recuperada em 20 pontos."


def evento_animal_selvagem(sobreviventes, inventario):
    vivos = [s for s in sobreviventes if s["vida"] > 0]
    if not vivos:
        return "Um animal selvagem rondou o acampamento, mas não havia ninguém."
    alvo = random.choice(vivos)
    dano = random.randint(10, 25)
    alvo["vida"] = max(0, alvo["vida"] - dano)
    return f"Um animal selvagem atacou {alvo['nome']}! Perdeu {dano} pontos de vida."


def evento_bau_escondido(sobreviventes, inventario):
    recurso = random.choice(RECURSOS_POSSIVEIS)
    quantidade = random.randint(3, 10)
    adicionar_ao_inventario(inventario, recurso, quantidade)
    return f"Baú escondido encontrado! Ganhou {quantidade}x {recurso}."


def evento_sobrevivente_perdido(sobreviventes, inventario):
    nomes_possiveis = ["Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gabriela"]
    nome = random.choice(nomes_possiveis)
    for s in sobreviventes:
        if s["nome"] == nome:
            return f"{nome} apareceu, mas já fazia parte do acampamento."
    sobreviventes.append({"nome": nome, "vida": 100, "fome": 80, "sede": 80})
    return f"Sobrevivente perdido chamado {nome} se juntou ao acampamento!"


def evento_tempestade_de_areia(sobreviventes, inventario):
    if inventario:
        item = random.choice(inventario)
        perda = min(item[1], random.randint(1, 4))
        item[1] -= perda
        return f"Tempestade de areia! Perdeu {perda}x {item[0]}."
    return "Tempestade de areia, mas o inventário já estava vazio."


MAPA_DE_EVENTOS = {
    "chuva": evento_chuva_forte,
    "animal": evento_animal_selvagem,
    "bau": evento_bau_escondido,
    "sobrevivente": evento_sobrevivente_perdido,
    "tempestade": evento_tempestade_de_areia,
}


def disparar_evento_aleatorio(sobreviventes, inventario):
    print(formatar_titulo("Evento Aleatório"))
    nome_evento = random.choice(list(MAPA_DE_EVENTOS.keys()))
    mensagem = MAPA_DE_EVENTOS[nome_evento](sobreviventes, inventario)
    print(mensagem)


def passar_o_tempo(sobreviventes):
    for s in sobreviventes:
        if s["vida"] <= 0:
            continue
        s["fome"] = max(0, s["fome"] - 3)
        s["sede"] = max(0, s["sede"] - 4)
        if s["fome"] == 0 or s["sede"] == 0:
            s["vida"] = max(0, s["vida"] - 10)
            print(f"{s['nome']} está sofrendo com fome/sede e perdeu vida!")


def exibir_menu():
    print(formatar_titulo("Simulador de Sobrevivência"))
    print("1 - Cadastrar sobrevivente")
    print("2 - Listar sobreviventes")
    print("3 - Explorar / Coletar recursos")
    print("4 - Ver inventário")
    print("5 - Construir item")
    print("6 - Ver itens construídos")
    print("7 - Avançar o tempo (evento aleatório)")
    print("0 - Sair")


def main():
    sobreviventes = []
    inventario = []
    itens_construidos = []
    mapa = gerar_mapa(TAMANHO_MAPA)

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
            print("Encerrando o simulador.")
            break
        else:
            print("Opção inválida.")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
