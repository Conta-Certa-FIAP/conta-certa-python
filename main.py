"""Conta Certa - Simulador de saída das dívidas.

Ponto de entrada do programa. Para executar: python main.py
"""

from arquivos import carregar_dados
from dividas import menu_dividas
from orcamento import configurar_orcamento, mostrar_diagnostico
from utilitarios import LINHA


def menu_principal(dados):
    """Menu principal. Repete até a pessoa escolher sair."""
    while True:
        print(f"\n{LINHA}")
        print(f"CONTA CERTA - Simulador de saída das dívidas")
        print(f"{LINHA}")
        print(f"1 - Minhas dívidas")
        print(f"2 - Meu orçamento")
        print(f"4 - Diagnóstico")
        print(f"0 - Sair")

        opcao = input(f"Escolha uma opção: ").strip()

        match opcao:
            case "1":
                menu_dividas(dados)
            case "2":
                configurar_orcamento(dados)
            case "4":
                mostrar_diagnostico(dados)
            case "0":
                print(f"\nAté logo! Seus dados estão salvos.")
                return
            case _:
                print(f"Opção inválida. Digite um número do menu.")


def main():
    """Carrega os dados salvos e abre o menu principal."""
    dados = carregar_dados()

    # Ctrl+C gera KeyboardInterrupt, e o fim da entrada gera EOFError. Tratamos os dois
    # para encerrar com uma mensagem clara. Nada se perde: cada alteração já foi salva.
    try:
        menu_principal(dados)
    except (KeyboardInterrupt, EOFError):
        print(f"\n\nPrograma encerrado. Seus dados estão salvos.")


# Este bloco só roda quando o arquivo é executado diretamente (python main.py),
# e não quando ele é importado por outro módulo.
if __name__ == "__main__":
    main()
