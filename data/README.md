# Dados

| Arquivo | Conteúdo |
|---|---|
| `clientes.csv` | 50.000 registros de 6.250 clientes (8 meses cada), já com o `score_credito` (Good / Standard / Poor). Usado para treinar e testar a IA. |
| `novos_clientes.csv` | 10 clientes novos, **sem** `score_credito` e sem `id_cliente`. A IA prevê o score deles. |

> **Os dados são sintéticos.** Nenhum registro corresponde a uma pessoa real. Eles foram gerados por um script que reproduz as distribuições e as relações entre as colunas de uma base real de clientes:
>
> - O perfil de cada cliente foi sorteado com uma cópula gaussiana, que mantém a distribuição de cada coluna e as correlações entre elas, mas cria combinações novas.
> - Os meses foram simulados como na base real: idade e histórico avançam, atrasos e saldo oscilam em torno da média do cliente.
> - O score foi sorteado a partir das probabilidades de um modelo treinado na base real, com persistência de um mês para o outro.

## Colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `id_cliente` | inteiro | Identificador do cliente (só em `clientes.csv`; não entra no modelo) |
| `mes` | inteiro | Mês do registro (cada cliente aparece em vários meses) |
| `idade` | número | Idade do cliente |
| `profissao` | texto | Profissão |
| `salario_anual` | número | Salário anual |
| `num_contas` | número | Quantidade de contas bancárias |
| `num_cartoes` | número | Quantidade de cartões de crédito |
| `juros_emprestimo` | número | Taxa de juros dos empréstimos |
| `num_emprestimos` | número | Quantidade de empréstimos |
| `dias_atraso` | número | Dias de atraso nos pagamentos |
| `num_pagamentos_atrasados` | número | Quantidade de pagamentos atrasados |
| `num_verificacoes_credito` | número | Quantas vezes o crédito foi consultado |
| `mix_credito` | texto | Avaliação do mix de crédito |
| `divida_total` | número | Dívida total |
| `taxa_uso_credito` | número | Percentual de uso do limite de crédito |
| `idade_historico_credito` | número | Idade do histórico de crédito (meses) |
| `investimento_mensal` | número | Valor investido por mês |
| `comportamento_pagamento` | texto | Perfil de gasto e pagamento |
| `saldo_final_mes` | número | Saldo no fim do mês |
| `score_credito` | texto | **Alvo**: Good, Standard ou Poor (só em `clientes.csv`) |
| `emprestimo_carro` | 0/1 | Tem empréstimo de carro |
| `emprestimo_casa` | 0/1 | Tem empréstimo imobiliário |
| `emprestimo_pessoal` | 0/1 | Tem empréstimo pessoal |
| `emprestimo_credito` | 0/1 | Tem empréstimo de crédito |
| `emprestimo_estudantil` | 0/1 | Tem empréstimo estudantil |
