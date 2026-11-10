"""Cadastro de dívidas: criar, listar, registrar pagamento e remover."""

from arquivos import salvar_dados
from utilitarios import (
    LINHA,
    VALOR_MAXIMO,
    formatar_moeda,
    formatar_numero,
    ler_confirmacao,
    ler_inteiro,
    ler_numero,
    ler_opcao,
    ler_texto,
)

# Usamos uma tupla porque os tipos válidos são fixos: a tupla não pode ser alterada
# durante a execução, o que protege esses valores contra mudanças por engano.
TIPOS_VALIDOS = ("CARTAO", "CARNE", "EMPRESTIMO", "CONTA", "OUTRO")

# Juros acima de 100% ao mês são recusados porque quase sempre são erro de digitação.
JUROS_MAXIMO = 100.0

# Cada opção do menu é um par (código, descrição). A tupla externa também é fixa.
OPCOES_MENU_DIVIDAS = (
    ("1", "Cadastrar dívida"),
    ("2", "Listar dívidas"),
    ("3", "Registrar pagamento"),
    ("4", "Remover dívida"),
    ("0", "Voltar"),
)


def criar_divida(credor, tipo, saldo, juros_mensal, parcela_minima):
    """Monta e devolve o dicionário que representa uma dívida.

    O dicionário permite acessar cada dado pelo nome, como divida["saldo"],
    o que deixa o código mais fácil de ler do que usar posições.
    """
    return {
        "credor": credor,
        "tipo": tipo,
        "saldo": saldo,
        "juros_mensal": juros_mensal,
        "parcela_minima": parcela_minima,
    }


def obter_credores_unicos(dividas):
    """Devolve um set com os credores, sem repetição."""
    # O set descarta repetições sozinho. Ele não é salvo no JSON porque esse formato
    # não tem o tipo set; por isso é sempre recalculado a partir da lista de dívidas.
    credores = set()
    for divida in dividas:
        credores.add(divida["credor"])
    return credores


def obter_dividas_ativas(dividas):
    """Devolve uma lista só com as dívidas que ainda têm saldo a pagar."""
    ativas = []
    for divida in dividas:
        if divida["saldo"] > 0:
            ativas.append(divida)
    return ativas


def somar_parcelas(dividas):
    """Devolve a soma das parcelas mínimas das dívidas que ainda estão ativas."""
    # Uma dívida quase quitada pode ter saldo menor que a parcela. Nesse caso só se paga
    # o saldo, por isso usamos o menor dos dois valores, como na simulação.
    total = 0.0
    for divida in obter_dividas_ativas(dividas):
        total = total + min(divida["parcela_minima"], divida["saldo"])
    return round(total, 2)


def somar_saldos(dividas):
    """Devolve a soma dos saldos de todas as dívidas."""
    total = 0.0
    for divida in dividas:
        total = total + divida["saldo"]
    return round(total, 2)


def ler_tipo():
    """Mostra os tipos válidos e devolve o tipo escolhido."""
    print(f"Tipos de dívida:")
    # enumerate entrega a posição junto com o item; start=1 faz a contagem começar em 1.
    for numero, tipo in enumerate(TIPOS_VALIDOS, start=1):
        print(f"  {numero} - {tipo}")

    indice = ler_inteiro(f"Número do tipo", 1, len(TIPOS_VALIDOS))
    # A pessoa vê a contagem a partir de 1, mas a tupla começa na posição 0.
    return TIPOS_VALIDOS[indice - 1]


def cadastrar_divida(dados):
    """Pede os dados de uma nova dívida, adiciona à lista e salva no arquivo."""
    print(f"\n--- Cadastrar dívida ---")

    # Credor em maiúsculas: "Nubank" e "nubank" contam como o mesmo credor no set.
    credor = ler_texto(f"Credor (a quem você deve)").upper()

    if credor in obter_credores_unicos(dados["dividas"]):
        print(f"Aviso: você já tem uma dívida com {credor}. Esta será cadastrada à parte.")

    tipo = ler_tipo()
    saldo = ler_numero(f"Saldo devedor em R$ (ex.: 1500,50)", 0.01, VALOR_MAXIMO)
    juros_mensal = ler_numero(f"Juros ao mês em % (ex.: 2,5 / 0 se não houver)", 0, JUROS_MAXIMO)
    # A parcela mínima usa o saldo como limite, já que não faz sentido ser maior que a dívida.
    parcela_minima = ler_numero(f"Parcela mínima em R$", 0.01, saldo)

    divida = criar_divida(credor, tipo, saldo, juros_mensal, parcela_minima)
    dados["dividas"].append(divida)
    salvar_dados(dados)

    print(f"Dívida com {credor} cadastrada: saldo de {formatar_moeda(saldo)}.")


def listar_dividas(dividas):
    """Mostra uma tabela com as dívidas, os totais e os credores únicos."""
    print(f"\n--- Minhas dívidas ---")

    if len(dividas) == 0:
        print(f"Nenhuma dívida cadastrada.")
        return

    # Nos f-strings, :<20 alinha à esquerda em 20 espaços e :>17 alinha à direita.
    # O .20 corta textos muito longos para não desalinhar a tabela.
    print(f"{'Nº':>2}  {'Credor':<20} {'Tipo':<10} {'Saldo':>17} {'Juros/mês':>9} {'Parcela':>14}")
    print(f"{LINHA}")

    for numero, divida in enumerate(dividas, start=1):
        if divida["saldo"] > 0:
            saldo_texto = formatar_moeda(divida["saldo"])
        else:
            saldo_texto = "QUITADA"

        juros_texto = f"{formatar_numero(divida['juros_mensal'])}%"
        parcela_texto = formatar_moeda(divida["parcela_minima"])

        print(
            f"{numero:>2}  {divida['credor']:<20.20} {divida['tipo']:<10} "
            f"{saldo_texto:>17} {juros_texto:>9} {parcela_texto:>14}"
        )

    print(f"{LINHA}")
    print(f"Saldo total: {formatar_moeda(somar_saldos(dividas))}")

    # sorted() devolve uma lista em ordem alfabética, pois o set não guarda ordem.
    credores = sorted(obter_credores_unicos(dividas))
    print(f"Credores únicos ({len(credores)}): {', '.join(credores)}")


def escolher_divida(dividas, mensagem):
    """Mostra as dívidas e devolve a posição da escolhida na lista, ou None se cancelar."""
    listar_dividas(dividas)
    numero = ler_inteiro(f"{mensagem} (0 para cancelar)", 0, len(dividas))

    if numero == 0:
        return None
    return numero - 1


def registrar_pagamento(dados):
    """Abate um pagamento do saldo de uma dívida e salva no arquivo."""
    dividas = dados["dividas"]

    if len(obter_dividas_ativas(dividas)) == 0:
        print(f"Não há dívidas ativas para receber pagamento.")
        return

    indice = escolher_divida(dividas, f"Número da dívida paga")
    if indice is None:
        print(f"Pagamento cancelado.")
        return

    divida = dividas[indice]
    if divida["saldo"] == 0:
        print(f"A dívida com {divida['credor']} já está quitada.")
        return

    # O saldo é o limite máximo para ninguém registrar um pagamento maior que a dívida.
    valor = ler_numero(f"Valor pago em R$", 0.01, divida["saldo"])

    # round evita resíduos do float, como 99.99000000000001.
    divida["saldo"] = round(divida["saldo"] - valor, 2)
    salvar_dados(dados)

    if divida["saldo"] == 0:
        print(f"Parabéns! A dívida com {divida['credor']} foi quitada.")
    else:
        print(f"Pagamento registrado. Novo saldo: {formatar_moeda(divida['saldo'])}.")


def remover_divida(dados):
    """Remove uma dívida da lista depois de pedir confirmação."""
    dividas = dados["dividas"]

    if len(dividas) == 0:
        print(f"Nenhuma dívida cadastrada.")
        return

    indice = escolher_divida(dividas, f"Número da dívida a remover")
    if indice is None:
        print(f"Remoção cancelada.")
        return

    credor = dividas[indice]["credor"]

    # A remoção não pode ser desfeita, então a pessoa precisa confirmar antes.
    if ler_confirmacao(f"Tem certeza de que deseja remover a dívida com {credor}?"):
        dividas.pop(indice)
        salvar_dados(dados)
        print(f"Dívida com {credor} removida.")
    else:
        print(f"Remoção cancelada.")


def menu_dividas(dados):
    """Submenu de dívidas. Repete até a pessoa escolher voltar."""
    while True:
        opcao = ler_opcao("MINHAS DÍVIDAS", OPCOES_MENU_DIVIDAS)

        # match-case compara a opção com cada "case"; o "case _" pega todo o resto.
        match opcao:
            case "1":
                cadastrar_divida(dados)
            case "2":
                listar_dividas(dados["dividas"])
            case "3":
                registrar_pagamento(dados)
            case "4":
                remover_divida(dados)
            case "0":
                return
            case _:
                print(f"Opção inválida. Digite um número do menu.")
