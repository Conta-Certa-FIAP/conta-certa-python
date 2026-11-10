"""Funções de apoio usadas pelos outros módulos.

Aqui ficam a leitura segura do teclado e a formatação de valores.
Elas estão separadas para não repetir o mesmo código em cada arquivo:
se uma regra de validação mudar, basta alterar neste único lugar.
"""

# Constantes ficam em maiúsculas por convenção: indicam valores que não mudam.
LINHA = "=" * 78

# Limite de segurança para valores em dinheiro. Além de barrar erros de digitação,
# ele recusa "inf" e "nan", textos que a função float() aceita como se fossem números.
VALOR_MAXIMO = 999_999_999.99


def formatar_numero(valor):
    """Devolve o número no padrão brasileiro com 2 casas. Ex.: 1234.5 vira 1.234,50."""
    # O f-string gera "1,234.50" (padrão americano). Trocamos os separadores usando
    # um caractere temporário (#) para que a primeira troca não atrapalhe a segunda.
    texto = f"{valor:,.2f}"
    return texto.replace(",", "#").replace(".", ",").replace("#", ".")


def formatar_moeda(valor):
    """Devolve o valor em reais com 2 casas. Ex.: 1234.5 vira R$ 1.234,50."""
    return f"R$ {formatar_numero(valor)}"


def converter_para_numero(texto):
    """Transforma o texto digitado em float, aceitando o formato brasileiro.

    Aceita "1500", "1500,50", "1.500,50", "1500.50" e "R$ 1.500".
    Se o texto não for um número, o float() gera ValueError, e quem chamou trata o erro.
    """
    limpo = texto.replace("R$", "").replace(" ", "")

    if "," in limpo:
        # Com vírgula, ela é o separador decimal e os pontos separam os milhares.
        limpo = limpo.replace(".", "").replace(",", ".")
    elif pontos_separam_milhares(limpo):
        # "1.500" no Brasil significa mil e quinhentos, e não 1,5.
        limpo = limpo.replace(".", "")

    return float(limpo)


def pontos_separam_milhares(texto):
    """Diz se os pontos do texto separam milhares, como em "1.500" e "1.500.000"."""
    # Sem vírgula, o ponto é ambíguo: "1.5" é um decimal, mas "1.500" é mil e quinhentos.
    # Tratamos como milhar quando todos os grupos depois do primeiro ponto têm 3 dígitos.
    partes = texto.split(".")

    if len(partes) == 1 or partes[0] == "":
        return False

    for grupo in partes[1:]:
        if len(grupo) != 3:
            return False
    return True


def ler_numero(mensagem, minimo, maximo, padrao=None):
    """Pede um número até receber um valor válido e o devolve com 2 casas decimais.

    Parâmetros:
        mensagem: texto mostrado para a pessoa.
        minimo e maximo: faixa de valores aceitos.
        padrao: valor usado se a pessoa só apertar Enter (None = Enter não é aceito).
    """
    # O while repete a pergunta porque não sabemos quantas tentativas serão necessárias.
    while True:
        texto = input(f"{mensagem}: ").strip()

        if texto == "" and padrao is not None:
            return padrao

        # O try/except impede que o programa quebre se a pessoa digitar letras.
        try:
            valor = converter_para_numero(texto)
        except ValueError:
            print(f"Valor inválido. Digite apenas números, por exemplo: 1500,50")
            continue

        if minimo <= valor <= maximo:
            return round(valor, 2)

        print(f"Digite um valor entre {formatar_numero(minimo)} e {formatar_numero(maximo)}.")


def ler_inteiro(mensagem, minimo, maximo):
    """Pede um número inteiro dentro da faixa informada e o devolve."""
    while True:
        texto = input(f"{mensagem}: ").strip()

        try:
            valor = int(texto)
        except ValueError:
            print(f"Valor inválido. Digite um número inteiro.")
            continue

        if minimo <= valor <= maximo:
            return valor

        print(f"Digite um número entre {minimo} e {maximo}.")


def ler_texto(mensagem):
    """Pede um texto que não pode ficar vazio e tira os espaços que sobram."""
    while True:
        # split() separa as palavras e join() as junta com um único espaço entre elas.
        # Assim, "  Casas   Bahia " vira "Casas Bahia".
        texto = " ".join(input(f"{mensagem}: ").split())

        if texto != "":
            return texto

        print(f"Este campo não pode ficar vazio.")


def ler_confirmacao(mensagem):
    """Faz uma pergunta de sim ou não e devolve True (sim) ou False (não)."""
    while True:
        resposta = input(f"{mensagem} (S/N): ").strip().upper()

        if resposta in ("S", "SIM"):
            return True
        elif resposta in ("N", "NAO", "NÃO"):
            return False
        else:
            print(f"Responda S para sim ou N para não.")


def ler_opcao(titulo, opcoes):
    """Mostra um menu e devolve a opção digitada, já sem espaços nas pontas.

    opcoes é uma tupla de pares (código, descrição), por exemplo:
    (("1", "Listar dívidas"), ("0", "Voltar")). Os menus só mudam de título
    e de opções, então esta função evita repetir os prints em cada um deles.
    """
    print(f"\n{LINHA}")
    print(f"{titulo}")
    print(f"{LINHA}")
    for codigo, descricao in opcoes:
        print(f"{codigo} - {descricao}")

    # A opção é lida como texto. Assim, uma letra não gera erro de conversão:
    # ela apenas cai no "case _" do menu, que trata qualquer opção inválida.
    return input(f"Escolha uma opção: ").strip()
