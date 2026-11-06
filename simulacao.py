"""Simulação dos planos de quitação: Avalanche e Bola de neve.

As funções de cálculo não usam print nem input: recebem valores e devolvem o resultado.
As funções de tela é que conversam com a pessoa. Com essa separação, a matemática pode
ser testada sozinha, e a comparação pode rodar os dois métodos sem mostrar nada no meio.
"""

from dividas import obter_dividas_ativas, somar_saldos
from orcamento import calcular_sobra
from utilitarios import LINHA, VALOR_MAXIMO, formatar_moeda, formatar_numero, ler_numero

# Regra do trabalho: a simulação para com aviso se passar de 360 meses (30 anos).
LIMITE_MESES = 360

# Um dicionário liga o nome usado no código ao nome mostrado na tela.
NOMES_METODOS = {"avalanche": "Avalanche", "bola_de_neve": "Bola de neve"}


def calcular_juros(saldo, taxa):
    """Devolve os juros de um mês. A taxa vem em porcentagem (2.5 significa 2,5%)."""
    return round(saldo * taxa / 100, 2)


def copiar_dividas_ativas(dividas):
    """Devolve cópias das dívidas ativas para a simulação trabalhar sem afetar as reais."""
    # Sem .copy(), as duas variáveis apontariam para o mesmo dicionário: a simulação
    # zeraria os saldos verdadeiros da pessoa, e a segunda simulação começaria errada.
    copias = []
    for divida in obter_dividas_ativas(dividas):
        copias.append(divida.copy())
    return copias


def tem_prioridade(candidata, atual, metodo):
    """Diz se a dívida candidata deve ser paga antes da dívida atual, segundo o método."""
    if metodo == "avalanche":
        # Avalanche: juros mais altos primeiro. No empate, o menor saldo decide.
        if candidata["juros_mensal"] != atual["juros_mensal"]:
            return candidata["juros_mensal"] > atual["juros_mensal"]
        return candidata["saldo"] < atual["saldo"]

    # Bola de neve: menor saldo primeiro. No empate, os juros mais altos decidem.
    if candidata["saldo"] != atual["saldo"]:
        return candidata["saldo"] < atual["saldo"]
    return candidata["juros_mensal"] > atual["juros_mensal"]


def escolher_prioritaria(dividas, metodo):
    """Devolve a dívida que deve receber o dinheiro extra, ou None se todas estão zeradas."""
    # Procuramos a melhor com um for, em vez de ordenar a lista. Começamos sem nenhuma
    # e trocamos sempre que encontramos uma dívida com mais prioridade do que a atual.
    prioritaria = None
    for divida in dividas:
        if divida["saldo"] > 0:
            if prioritaria is None or tem_prioridade(divida, prioritaria, metodo):
                prioritaria = divida
    return prioritaria


def pagar(divida, valor):
    """Abate até o valor informado do saldo e devolve quanto foi realmente pago."""
    # min() impede pagar mais do que se deve, o que deixaria o saldo negativo.
    pagamento = min(valor, divida["saldo"])
    divida["saldo"] = round(divida["saldo"] - pagamento, 2)
    return pagamento


def aplicar_juros_do_mes(dividas):
    """Soma os juros do mês ao saldo de cada dívida e devolve o total de juros."""
    total = 0.0
    for divida in dividas:
        juros = calcular_juros(divida["saldo"], divida["juros_mensal"])
        divida["saldo"] = round(divida["saldo"] + juros, 2)
        total = total + juros
    return round(total, 2)


def somar_minimas_do_mes(dividas):
    """Devolve quanto é preciso para pagar a parcela mínima de todas as dívidas."""
    # Uma dívida prestes a acabar pode ter saldo menor que a parcela; nesse caso
    # só é preciso pagar o saldo. Por isso usamos o menor entre os dois valores.
    total = 0.0
    for divida in dividas:
        total = total + min(divida["parcela_minima"], divida["saldo"])
    return round(total, 2)


def pagar_parcelas_minimas(dividas):
    """Paga a parcela mínima de cada dívida e devolve o total pago."""
    total = 0.0
    for divida in dividas:
        total = total + pagar(divida, divida["parcela_minima"])
    return round(total, 2)


def distribuir_sobra(dividas, sobra, metodo):
    """Entrega a sobra às dívidas prioritárias e devolve o total pago."""
    # Usamos while porque não sabemos quantas dívidas a sobra vai alcançar: se a
    # prioritária zerar e ainda houver dinheiro, ele passa para a próxima no mesmo mês.
    total = 0.0
    while sobra > 0:
        prioritaria = escolher_prioritaria(dividas, metodo)
        if prioritaria is None:
            break

        pagamento = pagar(prioritaria, sobra)
        sobra = round(sobra - pagamento, 2)
        total = total + pagamento
    return round(total, 2)


def montar_resultado(metodo, situacao, meses, total_juros, total_pago, quitacoes, valor_necessario):
    """Junta os dados da simulação em um único dicionário, que é o retorno do cálculo."""
    return {
        "metodo": metodo,
        "situacao": situacao,
        "meses": meses,
        "total_juros": total_juros,
        "total_pago": total_pago,
        "quitacoes": quitacoes,
        "valor_necessario": valor_necessario,
    }


def simular_plano(dividas, valor_mensal, metodo):
    """Simula o pagamento mês a mês e devolve um dicionário com o resultado.

    O campo "situacao" do resultado pode ser:
        "quitado": todas as dívidas foram pagas.
        "juros_nao_cobertos": o valor mensal não cobre os juros do mês.
        "minimas_nao_cobertas": o valor mensal não cobre as parcelas mínimas.
        "limite_de_meses": passaria de 360 meses.
    """
    ativas = copiar_dividas_ativas(dividas)
    mes = 0
    total_juros = 0.0
    total_pago = 0.0
    quitacoes = []  # Lista de tuplas (mês, credor), na ordem em que cada dívida acaba.

    # Usamos while porque não sabemos de antemão quantos meses serão necessários.
    while len(ativas) > 0:
        if mes == LIMITE_MESES:
            return montar_resultado(metodo, "limite_de_meses", mes, total_juros, total_pago, quitacoes, 0.0)

        mes = mes + 1

        # Passo 1: os juros incidem sobre o saldo de cada dívida.
        juros_do_mes = aplicar_juros_do_mes(ativas)
        total_juros = round(total_juros + juros_do_mes, 2)

        # Se o valor mensal for igual ou menor que os juros, a dívida total nunca
        # diminui. Continuar seria inútil, então paramos e avisamos.
        if valor_mensal <= juros_do_mes:
            return montar_resultado(metodo, "juros_nao_cobertos", mes, total_juros, total_pago, quitacoes, juros_do_mes)

        minimas_do_mes = somar_minimas_do_mes(ativas)
        if valor_mensal < minimas_do_mes:
            return montar_resultado(metodo, "minimas_nao_cobertas", mes, total_juros, total_pago, quitacoes, minimas_do_mes)

        # Passo 2: paga a parcela mínima de todas as dívidas.
        pago_nas_minimas = pagar_parcelas_minimas(ativas)

        # Passo 3: o que sobrou vai para a dívida prioritária. O valor mensal é sempre o
        # mesmo; assim, quando uma dívida acaba, a parcela dela vira sobra para a próxima.
        # É esse acúmulo que dá nome ao método "bola de neve".
        sobra = round(valor_mensal - pago_nas_minimas, 2)
        pago_na_sobra = distribuir_sobra(ativas, sobra, metodo)
        total_pago = round(total_pago + pago_nas_minimas + pago_na_sobra, 2)

        # Passo 4: registra as dívidas que zeraram e mantém na lista só as demais.
        ainda_ativas = []
        for divida in ativas:
            if divida["saldo"] == 0:
                quitacoes.append((mes, divida["credor"]))
            else:
                ainda_ativas.append(divida)
        ativas = ainda_ativas

    return montar_resultado(metodo, "quitado", mes, total_juros, total_pago, quitacoes, 0.0)


def comparar_planos(dividas, valor_mensal):
    """Simula os dois métodos e devolve uma tupla com os dois resultados."""
    # O método anterior não interfere no próximo: cada simulação cria as próprias cópias.
    avalanche = simular_plano(dividas, valor_mensal, "avalanche")
    bola_de_neve = simular_plano(dividas, valor_mensal, "bola_de_neve")
    return (avalanche, bola_de_neve)


def formatar_prazo(meses):
    """Devolve o prazo em texto. Ex.: 26 vira "26 meses (2 ano(s) e 2 mês(es))"."""
    # // é a divisão inteira, e % é o resto da divisão.
    anos = meses // 12
    meses_restantes = meses % 12

    if meses == 1:
        return f"1 mês"
    elif anos == 0:
        return f"{meses} meses"
    elif meses_restantes == 0:
        return f"{meses} meses ({anos} ano(s))"
    else:
        return f"{meses} meses ({anos} ano(s) e {meses_restantes} mês(es))"


def mostrar_aviso(resultado, valor_mensal):
    """Explica por que a simulação parou antes de quitar as dívidas."""
    nome = NOMES_METODOS[resultado["metodo"]]
    necessario = formatar_moeda(resultado["valor_necessario"])
    valor = formatar_moeda(valor_mensal)

    if resultado["situacao"] == "juros_nao_cobertos":
        print(f"AVISO ({nome}): no mês {resultado['meses']}, {valor} não cobrem os juros de {necessario}.")
        print(f"Com esse valor a dívida não diminui. Tente aumentar o valor ou renegociar os juros.")
    elif resultado["situacao"] == "minimas_nao_cobertas":
        print(f"AVISO ({nome}): no mês {resultado['meses']}, {valor} não cobrem as parcelas mínimas de {necessario}.")
        print(f"Tente aumentar o valor mensal ou renegociar as parcelas.")
    else:
        print(f"AVISO ({nome}): com {valor} por mês, a quitação passaria de {LIMITE_MESES} meses.")
        print(f"Tente aumentar o valor mensal ou renegociar os juros.")


def mostrar_plano(resultado, valor_mensal):
    """Mostra o resultado de um único método."""
    print(f"\n--- Plano {NOMES_METODOS[resultado['metodo']]} ---")

    if resultado["situacao"] != "quitado":
        mostrar_aviso(resultado, valor_mensal)
        return

    print(f"Valor mensal: {formatar_moeda(valor_mensal)}")
    print(f"Tempo até quitar: {formatar_prazo(resultado['meses'])}")
    print(f"Total pago em juros: {formatar_moeda(resultado['total_juros'])}")
    print(f"Total pago: {formatar_moeda(resultado['total_pago'])}")
    print(f"Ordem de quitação:")

    # Cada item da lista é uma tupla (mês, credor), e o for já separa os dois valores.
    for mes, credor in resultado["quitacoes"]:
        print(f"  Mês {mes:>3}: {credor}")


def mostrar_comparacao(avalanche, bola_de_neve, valor_mensal):
    """Mostra os dois métodos lado a lado e aponta o mais barato."""
    print(f"\n--- Comparação dos métodos ---")

    if avalanche["situacao"] != "quitado" or bola_de_neve["situacao"] != "quitado":
        print(f"Não foi possível comparar, pois pelo menos um dos planos não termina:")
        for resultado in (avalanche, bola_de_neve):
            if resultado["situacao"] != "quitado":
                mostrar_aviso(resultado, valor_mensal)
        return

    print(f"Valor mensal: {formatar_moeda(valor_mensal)}\n")
    print(f"{'':<24} {'Avalanche':>18} {'Bola de neve':>18}")
    print(f"{'Meses até quitar':<24} {avalanche['meses']:>18} {bola_de_neve['meses']:>18}")
    print(f"{'Total pago em juros':<24} {formatar_moeda(avalanche['total_juros']):>18} {formatar_moeda(bola_de_neve['total_juros']):>18}")
    print(f"{'Total pago':<24} {formatar_moeda(avalanche['total_pago']):>18} {formatar_moeda(bola_de_neve['total_pago']):>18}")

    # quitacoes[0] é a primeira tupla da lista, e o [0] seguinte é o mês dessa tupla.
    primeira_avalanche = avalanche["quitacoes"][0][0]
    primeira_bola = bola_de_neve["quitacoes"][0][0]
    print(f"{'1ª dívida quitada no mês':<24} {primeira_avalanche:>18} {primeira_bola:>18}\n")

    economia = round(bola_de_neve["total_juros"] - avalanche["total_juros"], 2)

    if economia > 0:
        print(f"A Avalanche economiza {formatar_moeda(economia)} em juros.")
    elif economia < 0:
        print(f"A Bola de neve economiza {formatar_moeda(-economia)} em juros.")
    else:
        print(f"Os dois métodos custam o mesmo em juros.")

    if primeira_bola < primeira_avalanche:
        print(f"A Bola de neve quita a primeira dívida antes, o que ajuda a manter a motivação.")


def pedir_valor_mensal(orcamento):
    """Pergunta quanto a pessoa pode pagar por mês, sugerindo a sobra do orçamento."""
    sobra = calcular_sobra(orcamento["renda"], orcamento["gastos_fixos"])

    if sobra > 0:
        return ler_numero(
            f"Valor mensal para as dívidas em R$ (Enter = {formatar_moeda(sobra)}, a sobra do orçamento)",
            0.01,
            VALOR_MAXIMO,
            sobra,
        )

    return ler_numero(f"Valor mensal para as dívidas em R$", 0.01, VALOR_MAXIMO)


def simular_opcao(dados, opcao):
    """Confere se há dívidas, pede o valor mensal e executa a opção escolhida."""
    if somar_saldos(dados["dividas"]) == 0:
        print(f"Não há dívidas ativas. Cadastre uma dívida em 'Minhas dívidas'.")
        return

    valor_mensal = pedir_valor_mensal(dados["orcamento"])

    match opcao:
        case "1":
            mostrar_plano(simular_plano(dados["dividas"], valor_mensal, "avalanche"), valor_mensal)
        case "2":
            mostrar_plano(simular_plano(dados["dividas"], valor_mensal, "bola_de_neve"), valor_mensal)
        case "3":
            avalanche, bola_de_neve = comparar_planos(dados["dividas"], valor_mensal)
            mostrar_comparacao(avalanche, bola_de_neve, valor_mensal)


def menu_simulacao(dados):
    """Submenu de simulação. Repete até a pessoa escolher voltar."""
    while True:
        print(f"\n{LINHA}")
        print(f"SIMULAR PLANO DE QUITAÇÃO")
        print(f"{LINHA}")
        print(f"1 - Avalanche (paga primeiro os juros mais altos)")
        print(f"2 - Bola de neve (paga primeiro o menor saldo)")
        print(f"3 - Comparar os dois")
        print(f"0 - Voltar")

        opcao = input(f"Escolha uma opção: ").strip()

        # O caractere | significa "ou": os três casos seguem pelo mesmo caminho.
        match opcao:
            case "1" | "2" | "3":
                simular_opcao(dados, opcao)
            case "0":
                return
            case _:
                print(f"Opção inválida. Digite um número do menu.")
