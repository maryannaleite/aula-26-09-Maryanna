import os

MAGENTA = "\033[1;35m"
AMARELO = "\033[1;33m"
VERMELHO = "\033[1;31m"
VERDE = "\033[1;32m"
RESET = "\033[0m"

def texto_magenta(mensagem):
    return f"{MAGENTA}{mensagem}{RESET}"

def texto_vermelho(mensagem):
    return f"{VERMELHO}{mensagem}{RESET}"

def texto_amarelo(mensagem):
    return f"{AMARELO}{mensagem}{RESET}"

def texto_verde(mensagem):
    return f"{VERDE}{mensagem}{RESET}"

def carregar_arquivos(nome_arquivos):
    if os.path.exists(nome_arquivos):
        with open(nome_arquivos, "r", encoding="utf-8") as file:
            return [linha.strip().split(";") for linha in file.readlines()]
    return []

def salvar_arquivo(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        for linha in dados:
            file.write(';'.join(str(x) for x in linha) + '\n')

def cadastrar_produto():
    produtos = carregar_arquivos('produtos.txt')
    codigo = input("Código do produto: ")
    nome = input("Nome do produto: ")
    descricao = input("Descrição do produto: ")

    for produto in produtos:
        if produto[0] == codigo:
            print("Já existe um produto com esse código.")
            return

    try:
        preco_compra = float(input("Preço de compra: "))
        preco_venda = float(input("Preço de venda: "))
    except ValueError:
        print(texto_vermelho("Valor inválido para preço. Tente novamente."))
        return

    if preco_venda <= preco_compra:
        print(texto_vermelho("O preço de venda deve ser maior que o preço de compra."))
        return

    produtos.append([codigo, nome, descricao, preco_compra, preco_venda])
    salvar_arquivo('produtos.txt', produtos)
    print(texto_verde(f"O produto {nome} foi cadastrado com sucesso!"))

def remover_produto():
    produtos = carregar_arquivos('produtos.txt')
    codigo = input("Código do produto a ser removido: ")

    produtos = [produto for produto in produtos if produto[0] != codigo]
    salvar_arquivo('produtos.txt', produtos)

    for arquivo in ['compras.txt', 'vendas.txt']:
        itens = carregar_arquivos(arquivo)
        itens = [item for item in itens if item[2] != codigo]
        salvar_arquivo(arquivo, itens)

    print(texto_verde("Produto removido com sucesso!"))

def atualizar_produto():
    produtos = carregar_arquivos('produtos.txt')
    codigo = input("Código do produto a ser atualizado: ")

    for produto in produtos:
        if produto[0] == codigo:
            nome = input(f"Nome ({produto[1]}): ") or produto[1]
            descricao = input(f"Descrição ({produto[2]}): ") or produto[2]

            while True:
                try:
                    preco_compra = float(input(f"Preço de compra ({produto[3]}): ") or produto[3])
                    preco_venda = float(input(f"Preço de venda ({produto[4]}): ") or produto[4])
                    if preco_venda <= preco_compra:
                        print(texto_vermelho("O preço de venda deve ser maior que o preço de compra."))
                    else:
                        break
                except ValueError:
                    print(texto_vermelho("Valor inválido. Tente novamente."))

            produto[1] = nome
            produto[2] = descricao
            produto[3] = preco_compra
            produto[4] = preco_venda
            break
    else:
        print(texto_vermelho("Produto não encontrado."))
        return

    salvar_arquivo('produtos.txt', produtos)
    print(texto_verde(f"Produto {codigo} atualizado com sucesso!"))