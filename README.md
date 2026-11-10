# ContaTech - Simulador de saída das dívidas

Programa de terminal feito para a Global Solution da FIAP (2026/2), na disciplina
Computational Thinking Using Python. Faz parte da solução CitizenTech **ContaTech**,
voltada a famílias de baixa renda endividadas. Funciona de forma independente: não se
conecta à API Java nem ao front-end do projeto.

## O que o programa faz

- **Minhas dívidas:** cadastra, lista, registra pagamentos e remove dívidas, com confirmação antes de remover.
- **Meu orçamento:** guarda a renda mensal e os gastos fixos e mostra quanto sobra por mês.
- **Simular plano de quitação:** calcula mês a mês os métodos Avalanche (juros mais altos primeiro) e Bola de neve (menor saldo primeiro) e compara os dois em meses até quitar e total pago em juros.
- **Diagnóstico:** mostra a porcentagem da renda comprometida com parcelas: até 30% é saudável, até 50% pede atenção e acima disso é crítico.

Os dados ficam salvos no arquivo `dados_contatech.json`, criado automaticamente na
pasta do projeto e atualizado a cada alteração. Esse arquivo não vai para o repositório.

## Como rodar

É preciso ter o **Python 3.10 ou mais recente**, pois o programa usa `match-case`.
Nenhuma biblioteca externa é necessária.

```bash
python main.py
```

Se o terminal não reconhecer `python`, use o comando do Python instalado no seu
computador, como `py main.py` ou `python3 main.py`.

## Estrutura de arquivos

```text
conta-certa-python/
├── main.py            # Ponto de entrada e menu principal
├── dividas.py         # Cadastro, listagem, pagamento e remoção de dívidas
├── orcamento.py       # Renda, gastos fixos e diagnóstico
├── simulacao.py       # Cálculo e telas dos métodos Avalanche e Bola de neve
├── arquivos.py        # Leitura e gravação do arquivo JSON
├── utilitarios.py     # Validação de entradas, menus e formatação de valores
├── integrantes.txt    # Nome, RM e turma dos integrantes
└── docs/
    └── documentacao.md  # Conteúdo do PDF de entrega
```
