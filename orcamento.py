"""Orçamento da família e diagnóstico do comprometimento da renda."""

from arquivos import salvar_dados
from dividas import somar_parcelas
from utilitarios import LINHA, VALOR_MAXIMO, formatar_moeda, formatar_numero, ler_numero


def calcular_sobra(renda, gastos_fixos):
    """Devolve quanto sobra da renda depois dos gastos fixos."""
    return round(renda - gastos_fixos, 2)


def calcular_comprometimento(total_parcelas, renda):
    """Devolve a porcentagem da renda usada para pagar as parcelas.

    Só deve ser chamada com renda maior que zero, para evitar divisão por zero.
    Quem garante isso é a função mostrar_diagnostico, que testa a renda antes.
    """
    return round(total_parcelas / renda * 100, 2)


def avaliar_comprometimento(percentual):
    """Devolve uma tupla com a situação e uma orientação, de acordo com o percentual."""
    # Aqui usamos if-elif-else, e não match-case, porque testamos faixas de valores
    # (menor ou igual a 30, por exemplo). Basta entrar em uma condição para as outras
    # serem ignoradas; por isso o elif não precisa repetir "maior que 30".
    if percentual <= 30:
        return ("SAUDÁVEL", "As parcelas cabem na renda. Mantenha os pagamentos em dia.")
    elif percentual <= 50:
        return ("ATENÇÃO", "As parcelas pesam na renda. Evite novas dívidas e priorize quitar.")
    else:
        return ("CRÍTICO", "As parcelas tomam boa parte da renda. Busque renegociar com os credores.")


def configurar_orcamento(dados):
    """Pede a renda e os gastos fixos, salva e mostra quanto sobra por mês."""
    orcamento = dados["orcamento"]

    print(f"\n--- Meu orçamento ---")
    print(f"Renda atual: {formatar_moeda(orcamento['renda'])}")
    print(f"Gastos fixos atuais: {formatar_moeda(orcamento['gastos_fixos'])}")
    print(f"Aperte Enter para manter o valor atual.")

    orcamento["renda"] = ler_numero(f"Renda mensal em R$", 0, VALOR_MAXIMO, orcamento["renda"])

    # As parcelas ficam de fora dos gastos fixos, pois a sobra será usada para pagá-las.
    # Se elas entrassem aqui, seriam contadas duas vezes na simulação.
    orcamento["gastos_fixos"] = ler_numero(
        f"Gastos fixos em R$ (sem as parcelas das dívidas)",
        0,
        VALOR_MAXIMO,
        orcamento["gastos_fixos"],
    )
    salvar_dados(dados)

    sobra = calcular_sobra(orcamento["renda"], orcamento["gastos_fixos"])

    if sobra > 0:
        print(f"Orçamento salvo. Sobram {formatar_moeda(sobra)} por mês para pagar as dívidas.")
    elif sobra == 0:
        print(f"Orçamento salvo. Não sobra nada para pagar as dívidas.")
    else:
        print(f"Orçamento salvo. Os gastos passam da renda em {formatar_moeda(-sobra)}.")


def mostrar_diagnostico(dados):
    """Mostra a porcentagem da renda comprometida com as parcelas e a situação."""
    renda = dados["orcamento"]["renda"]

    print(f"\n{LINHA}")
    print(f"DIAGNÓSTICO")
    print(f"{LINHA}")

    if renda <= 0:
        print(f"Informe sua renda em 'Meu orçamento' para ver o diagnóstico.")
        return

    total_parcelas = somar_parcelas(dados["dividas"])
    percentual = calcular_comprometimento(total_parcelas, renda)
    # Uma função pode devolver uma tupla, e seus itens podem ir para variáveis separadas.
    situacao, orientacao = avaliar_comprometimento(percentual)

    print(f"Renda mensal: {formatar_moeda(renda)}")
    print(f"Soma das parcelas: {formatar_moeda(total_parcelas)}")
    print(f"Renda comprometida: {formatar_numero(percentual)}%")
    print(f"Situação: {situacao}")
    print(f"{orientacao}")

    sobra = calcular_sobra(renda, dados["orcamento"]["gastos_fixos"])
    if total_parcelas > 0 and sobra < total_parcelas:
        print(f"Aviso: a renda menos os gastos fixos ({formatar_moeda(sobra)}) não cobre as parcelas.")
