"""Persistência: lê e grava os dados do programa em um arquivo JSON."""

import json
import os

# __file__ é o caminho deste arquivo .py. Montamos o caminho a partir dele para que os
# dados fiquem sempre na pasta do projeto, de qualquer pasta que o programa seja aberto.
PASTA_DO_PROJETO = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DADOS = os.path.join(PASTA_DO_PROJETO, "dados_contatech.json")
CAMINHO_TEMPORARIO = CAMINHO_DADOS + ".tmp"
CAMINHO_COPIA_INVALIDA = os.path.join(PASTA_DO_PROJETO, "dados_contatech.invalido.json")

# Campos que toda dívida precisa ter para o programa funcionar.
CAMPOS_TEXTO_DIVIDA = ("credor", "tipo")
CAMPOS_NUMERO_DIVIDA = ("saldo", "juros_mensal", "parcela_minima")


def criar_dados_iniciais():
    """Devolve a estrutura vazia usada quando ainda não há dados salvos.

    Tudo fica em um único dicionário, que é passado de função em função.
    Assim o programa não precisa de variáveis globais.
    """
    return {
        "dividas": [],
        "orcamento": {"renda": 0.0, "gastos_fixos": 0.0},
    }


def salvar_dados(dados):
    """Grava os dados no arquivo. É chamada logo após cada alteração."""
    # Gravamos primeiro em um arquivo temporário e só depois o renomeamos para o nome
    # definitivo. Se o computador desligar no meio da gravação, o arquivo antigo
    # continua inteiro, em vez de ficar pela metade.
    # O "with" fecha o arquivo sozinho, mesmo se ocorrer um erro durante a gravação.
    # ensure_ascii=False mantém os acentos legíveis e indent=2 organiza o arquivo.
    try:
        with open(CAMINHO_TEMPORARIO, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        os.replace(CAMINHO_TEMPORARIO, CAMINHO_DADOS)
    except OSError as erro:
        # OSError cobre problemas como falta de permissão ou disco cheio.
        print(f"ATENÇÃO: não foi possível salvar os dados: {erro}")


def eh_numero(valor):
    """Diz se o valor é um número (int ou float)."""
    # Em Python, bool é um tipo de int (True vale 1), por isso o excluímos de propósito.
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def divida_eh_valida(divida):
    """Confere se uma dívida lida do arquivo tem todos os campos com os tipos certos."""
    if not isinstance(divida, dict):
        return False

    for campo in CAMPOS_TEXTO_DIVIDA:
        if not isinstance(divida.get(campo), str):
            return False

    for campo in CAMPOS_NUMERO_DIVIDA:
        if not eh_numero(divida.get(campo)):
            return False

    return True


def dados_sao_validos(dados):
    """Confere se o conteúdo do arquivo tem a estrutura que o programa espera.

    Um JSON pode ser válido e mesmo assim não servir: alguém pode ter editado o
    arquivo à mão e apagado um campo. Sem esta checagem, o erro só apareceria
    mais tarde, no meio de uma listagem ou de uma simulação.
    """
    if not isinstance(dados, dict):
        return False

    dividas = dados.get("dividas")
    orcamento = dados.get("orcamento")
    if not isinstance(dividas, list) or not isinstance(orcamento, dict):
        return False

    if not eh_numero(orcamento.get("renda")) or not eh_numero(orcamento.get("gastos_fixos")):
        return False

    for divida in dividas:
        if not divida_eh_valida(divida):
            return False

    return True


def carregar_dados():
    """Lê os dados do arquivo e cria um arquivo novo se ele não existir."""
    if not os.path.exists(CAMINHO_DADOS):
        dados = criar_dados_iniciais()
        salvar_dados(dados)
        return dados

    # json.JSONDecodeError: o conteúdo não é um JSON válido.
    # UnicodeDecodeError: o arquivo não está em UTF-8.
    # OSError: o arquivo existe, mas não pôde ser lido (por exemplo, sem permissão).
    try:
        with open(CAMINHO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return recomecar_com_arquivo_invalido()

    if not dados_sao_validos(dados):
        return recomecar_com_arquivo_invalido()

    return dados


def recomecar_com_arquivo_invalido():
    """Guarda uma cópia do arquivo com problema e recomeça com dados vazios.

    O arquivo é renomeado em vez de apagado para que a pessoa não perca
    informações que ainda poderiam ser recuperadas manualmente.
    """
    print(f"ATENÇÃO: o arquivo de dados estava com problema e o programa recomeçou vazio.")

    try:
        os.replace(CAMINHO_DADOS, CAMINHO_COPIA_INVALIDA)
        print(f"Uma cópia do arquivo antigo foi guardada em: {CAMINHO_COPIA_INVALIDA}")
    except OSError as erro:
        print(f"Não foi possível guardar uma cópia do arquivo antigo: {erro}")

    dados = criar_dados_iniciais()
    salvar_dados(dados)
    return dados
