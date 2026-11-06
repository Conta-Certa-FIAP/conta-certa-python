# Conta Certa: Simulador de Saída das Dívidas

**FIAP - Análise e Desenvolvimento de Sistemas - 1º ano**

**Disciplina:** Computational Thinking Using Python

**Entrega:** Global Solution 2026/2

**Turma:** ____________

| Integrante | RM |
|------------|----|
|            |    |
|            |    |
|            |    |
|            |    |
|            |    |

**Repositório:** <https://github.com/Conta-Certa-FIAP/conta-certa-python>

---

## Sumário

1. [Descrição do problema](#1-descrição-do-problema)
2. [Objetivos](#2-objetivos)
3. [Justificativa](#3-justificativa)
4. [Escopo](#4-escopo)
5. [Funcionalidades implementadas](#5-funcionalidades-implementadas)
6. [Lógica aplicada](#6-lógica-aplicada)
7. [Resultados esperados](#7-resultados-esperados)
8. [Instruções de execução](#8-instruções-de-execução)

---

## 1. Descrição do problema

Muitas famílias de baixa renda acumulam dívidas de naturezas diferentes ao mesmo tempo,
como cartão de crédito, carnê de loja, empréstimo e contas atrasadas. Cada uma tem um
saldo, uma taxa de juros e uma parcela próprios. Sem uma visão do conjunto, é difícil
saber quanto da renda já está comprometido, qual dívida atacar primeiro e quanto tempo
levará para sair dessa situação.

Essa falta de clareza tem um custo real: o dinheiro extra pode ir para uma dívida barata
enquanto outra, com juros muito mais altos, continua crescendo.

## 2. Objetivos

**Objetivo geral:** ajudar a família endividada a enxergar suas dívidas e a montar um
plano de quitação possível dentro do próprio orçamento.

**Objetivos específicos:**

- Reunir todas as dívidas em um só lugar, com registro dos pagamentos.
- Calcular quanto sobra da renda depois dos gastos fixos.
- Simular a quitação pelos métodos Avalanche e Bola de neve.
- Comparar os métodos em prazo e total pago em juros.
- Mostrar o nível de comprometimento da renda de forma simples.
- Avisar quando o valor mensal não é suficiente para sair da dívida.

## 3. Justificativa

O Conta Certa é uma solução CitizenTech: usa a tecnologia para resolver um problema
concreto de cidadania financeira. Este simulador transforma uma conta difícil de fazer à
mão, com juros que mudam o saldo todos os meses, em uma resposta direta: em quanto tempo
a dívida acaba e quanto será pago em juros em cada caminho.

O programa roda no terminal e usa apenas a biblioteca padrão do Python, por isso não
exige internet nem a instalação de pacotes adicionais. Os dados ficam no próprio
computador, em um arquivo local.

## 4. Escopo

**Dentro do escopo:**

- Programa de terminal independente, com dados salvos em arquivo JSON local.
- Cadastro e acompanhamento de dívidas, orçamento, simulação e diagnóstico.

**Fora do escopo:**

- Integração com a API Java e com o front-end do Conta Certa.
- Conexão com bancos, negociação com credores e pagamentos reais.
- Multas por atraso, mudanças futuras de taxa e novas compras. A simulação considera
  juros fixos e o mesmo valor pago em todos os meses, então o resultado é uma estimativa.

## 5. Funcionalidades implementadas

| Menu | Funcionalidade | Comportamento |
|------|----------------|---------------|
| 1 - Minhas dívidas | Cadastrar | Pede credor, tipo, saldo, juros ao mês e parcela mínima |
| | Listar | Mostra uma tabela, o saldo total e os credores únicos |
| | Registrar pagamento | Abate o valor do saldo; dívida com saldo zero aparece como quitada |
| | Remover | Pede confirmação antes de apagar |
| 2 - Meu orçamento | Renda e gastos fixos | Guarda os valores e mostra a sobra mensal |
| 3 - Simular plano | Avalanche | Paga primeiro a dívida com juros mais altos |
| | Bola de neve | Paga primeiro a dívida de menor saldo |
| | Comparar | Mostra meses até quitar e total pago em juros de cada método |
| 4 - Diagnóstico | Comprometimento | Até 30%: saudável; até 50%: atenção; acima: crítico |
| 0 - Sair | | Encerra o programa |

## 6. Lógica aplicada

### 6.1 Simulação mês a mês

A função `simular_plano(dividas, valor_mensal, metodo)` repete os passos abaixo até
todas as dívidas acabarem:

1. Aplica os juros do mês em cada dívida, com `calcular_juros(saldo, taxa)`.
2. Verifica se o valor mensal cobre os juros e as parcelas mínimas. Se não cobrir, para com aviso.
3. Paga a parcela mínima de todas as dívidas.
4. Entrega o que sobrou à dívida prioritária. Se ela zerar e ainda houver dinheiro, o restante vai para a próxima no mesmo mês.
5. Retira da lista as dívidas quitadas e registra o mês em que cada uma acabou.

O valor mensal é o mesmo em todos os meses. Por isso, quando uma dívida acaba, a parcela
dela passa automaticamente a reforçar a próxima prioridade.

**Exemplo:** uma dívida de R$ 100,00 a 10% ao mês, pagando R$ 60,00 por mês:

| Mês | Saldo + juros | Pagamento | Saldo final |
|-----|---------------|-----------|-------------|
| 1 | 100,00 + 10,00 = 110,00 | 60,00 | 50,00 |
| 2 | 50,00 + 5,00 = 55,00 | 55,00 | 0,00 |

Resultado: 2 meses, R$ 15,00 de juros e R$ 115,00 pagos no total.

### 6.2 Critérios de prioridade

- **Avalanche:** maior taxa de juros; no empate, menor saldo.
- **Bola de neve:** menor saldo; no empate, maior taxa de juros.

A prioridade é calculada de novo a cada mês, pois os saldos mudam.

### 6.3 Quando a simulação para com aviso

| Situação | Motivo |
|----------|--------|
| Valor mensal igual ou menor que os juros do mês | A dívida total não diminuiria |
| Valor mensal menor que a soma das parcelas mínimas | Não seria possível pagar a parcela mínima de todas |
| Mais de 360 meses | Limite definido para o plano (30 anos) |

### 6.4 Conceitos de programação utilizados

| Conceito | Onde é usado |
|----------|--------------|
| `while` | Menus, leitura repetida de entradas e meses da simulação, cujo total não é conhecido de antemão |
| `for` | Percorrer as dívidas, somar valores e mostrar listas |
| `match-case` | Menu principal e submenus |
| `if-elif-else` | Diagnóstico, avisos da simulação e mensagens do orçamento |
| Lista | Conjunto das dívidas e ordem de quitação |
| Dicionário | Cada dívida, o orçamento e o resultado da simulação |
| Tupla | Tipos válidos, pares (mês, credor) e retorno de duas informações em uma função |
| Set | Credores únicos, recalculados a partir da lista |
| String | Tratamento de textos digitados e formatação dos valores em R$ |
| Funções | Todo o programa, com parâmetros e retorno |
| `try/except` | Validação de números e tratamento de erros de arquivo |
| Arquivo JSON | Dados salvos a cada alteração e criados se não existirem |

### 6.5 Organização do código

| Arquivo | Responsabilidade |
|---------|------------------|
| `main.py` | Início do programa e menu principal |
| `dividas.py` | Regras e telas de dívidas |
| `orcamento.py` | Orçamento e diagnóstico |
| `simulacao.py` | Cálculo e telas dos planos de quitação |
| `arquivos.py` | Leitura e gravação do JSON |
| `utilitarios.py` | Validação de entradas e formatação, compartilhadas pelos módulos |

## 7. Resultados esperados

Com o simulador, a família deve conseguir entender a própria situação e decidir com
base em números, sabendo qual método combina mais com suas prioridades.

O exemplo abaixo foi gerado pelo próprio programa, com dados fictícios: renda de
R$ 3.000,00 e gastos fixos de R$ 2.200,00, o que deixa R$ 800,00 por mês para as dívidas.

| Credor | Tipo | Saldo | Juros ao mês | Parcela mínima |
|--------|------|-------|--------------|----------------|
| NUBANK | CARTAO | R$ 3.000,00 | 12,00% | R$ 150,00 |
| CASAS LAR | CARNE | R$ 600,00 | 5,00% | R$ 60,00 |
| BANCO POPULAR | EMPRESTIMO | R$ 5.000,00 | 3,00% | R$ 200,00 |
| COMPANHIA DE LUZ | CONTA | R$ 250,00 | 1,00% | R$ 50,00 |

| Resultado | Avalanche | Bola de neve |
|-----------|-----------|--------------|
| Meses até quitar | 18 | 19 |
| Total pago em juros | R$ 4.903,02 | R$ 5.741,42 |
| Total pago | R$ 13.753,02 | R$ 14.591,42 |
| 1ª dívida quitada no mês | 6 | 1 |

Neste caso, a Avalanche economiza R$ 838,40 em juros e termina um mês antes. A Bola de
neve quita a primeira dívida já no mês 1, o que pode ajudar a família a manter a
motivação. O diagnóstico mostra 15,33% da renda comprometida com parcelas: situação
**saudável**.

## 8. Instruções de execução

1. Instale o Python 3.10 ou mais recente. Não é preciso instalar bibliotecas.
2. Baixe o projeto:

   ```bash
   git clone https://github.com/Conta-Certa-FIAP/conta-certa-python.git
   cd conta-certa-python
   ```

3. Execute o programa:

   ```bash
   python main.py
   ```

4. Use os números dos menus para navegar. Valores podem ser digitados como `1500,50` ou `1.500,50`.

O arquivo `dados_conta_certa.json` é criado na primeira execução, na pasta do projeto.
