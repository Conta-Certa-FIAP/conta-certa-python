"""Persistência: lê e grava os dados do programa em um arquivo JSON."""

import json
import os

# __file__ é o caminho deste arquivo .py. Montamos o caminho a partir dele para que os
# dados fiquem sempre na pasta do projeto, de qualquer pasta que o programa seja aberto.
PASTA_DO_PROJETO = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DADOS = os.path.join(PASTA_DO_PROJETO, "dados_conta_certa.json")
CAMINHO_COPIA_INVALIDA = os.path.join(PASTA_DO_PROJETO, "dados_conta_certa.invalido.json")


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
    # O "with" fecha o arquivo sozinho, mesmo se ocorrer um erro durante a gravação.
    # ensure_ascii=False mantém os acentos legíveis e indent=2 organiza o arquivo.
    try:
        with open(CAMINHO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    except OSError as erro:
        # OSError cobre problemas como falta de permissão ou disco cheio.
        print(f"ATENÇÃO: não foi possível salvar os dados: {erro}")


def carregar_dados():
    """Lê os dados do arquivo e cria um arquivo novo se ele não existir."""
    if not os.path.exists(CAMINHO_DADOS):
        dados = criar_dados_iniciais()
        salvar_dados(dados)
        return dados

    # json.JSONDecodeError: o conteúdo não é um JSON válido.
    # UnicodeDecodeError: o arquivo não está em UTF-8.
    try:
        with open(CAMINHO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return recomecar_com_arquivo_invalido()

    # Um JSON pode ser válido e mesmo assim não ter o formato que o programa espera.
    if not isinstance(dados, dict) or "dividas" not in dados or "orcamento" not in dados:
        return recomecar_com_arquivo_invalido()

    return dados


def recomecar_com_arquivo_invalido():
    """Guarda uma cópia do arquivo com problema e recomeça com dados vazios.

    O arquivo é renomeado em vez de apagado para que a pessoa não perca
    informações que ainda poderiam ser recuperadas manualmente.
    """
    os.replace(CAMINHO_DADOS, CAMINHO_COPIA_INVALIDA)
    print(f"ATENÇÃO: o arquivo de dados estava com problema e o programa recomeçou vazio.")
    print(f"Uma cópia do arquivo antigo foi guardada em: {CAMINHO_COPIA_INVALIDA}")

    dados = criar_dados_iniciais()
    salvar_dados(dados)
    return dados
