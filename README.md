# IA de Score de Crédito

Modelo de machine learning que classifica o score de crédito de clientes de um banco em **Good**, **Standard** ou **Poor**, a partir de dados cadastrais e de comportamento financeiro (salário, dívidas, atrasos, empréstimos etc.). O modelo treinado é usado para prever o score de clientes novos.

## Sobre os dados

A base tem 50.000 registros mensais de 6.250 clientes (8 meses por cliente) e 10 clientes novos para a IA classificar.

**Os dados são sintéticos:** nenhum registro corresponde a uma pessoa real. Eles foram gerados a partir das estatísticas de uma base real de clientes, mantendo as distribuições das colunas, as correlações entre elas e a relação com o score. Detalhes e descrição das colunas em [data/README.md](data/README.md).

## Tecnologias

- Python
- pandas
- scikit-learn (Random Forest, KNN, Pipeline)
- matplotlib
- Jupyter Notebook

## Estrutura do projeto

```
ia-score-de-credito/
├── data/
│   ├── README.md                  # como os dados foram gerados e descrição das colunas
│   ├── clientes.csv               # histórico de clientes com score (treino/teste)
│   └── novos_clientes.csv         # clientes para a IA classificar
├── models/                        # modelo treinado (gerado pelo script de treino)
├── notebooks/
│   └── IA_de_score_de_credito.ipynb   # análise passo a passo, com gráficos
├── src/
│   ├── config.py                  # caminhos, colunas e parâmetros
│   ├── modelo.py                  # preparo dos dados e criação dos modelos
│   ├── treinar.py                 # treina, compara e salva o melhor modelo
│   └── prever.py                  # usa o modelo salvo em novos clientes
├── requirements.txt
└── LICENSE
```

## Como rodar

**1. Clone o repositório, entre na pasta e crie um ambiente virtual**

```bash
cd ia-score-de-credito
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

**2. Treine o modelo**

```bash
python -m src.treinar
python -m src.treinar --dados caminho/para/clientes.csv
```

O script compara Random Forest e KNN, mostra a acurácia e o relatório de cada classe e salva o melhor modelo em `models/modelo_score.joblib` (as métricas ficam em `models/metricas.json`).

**3. Preveja o score dos novos clientes**

```bash
python -m src.prever
python -m src.prever data/novos_clientes.csv --saida data/previsoes.csv   # salvando em CSV
```

**Ou abra o notebook** para ver a análise completa com explicações e gráficos:

```bash
jupyter notebook notebooks/IA_de_score_de_credito.ipynb
```

## Como funciona

1. **Preparo:** as colunas de texto (`profissao`, `mix_credito`, `comportamento_pagamento`) são convertidas em números. Para o KNN, as colunas numéricas também são padronizadas, porque ele mede distâncias e o salário, na casa dos milhares, dominaria as outras variáveis.
2. **Divisão treino/teste:** 70% dos clientes para treino e 30% para teste, **separando por cliente** (cada cliente tem vários meses de registros e não pode aparecer nos dois lados).
3. **Treino e comparação:** Random Forest e KNN são treinados e comparados pela acurácia no teste.
4. **Modelo final:** o melhor modelo é treinado de novo com todos os dados e salvo, junto com a etapa de preparo, em um único arquivo.
5. **Previsão:** o modelo salvo recebe os novos clientes e devolve o score previsto, sem precisar treinar de novo.

## Resultados

Acurácia no conjunto de teste:

| Divisão treino/teste | Random Forest | KNN |
|---|---|---|
| Por linha (como na primeira versão) | 80,3% | 76,0% |
| **Por cliente (versão atual)** | **64,0%** | **54,9%** |

O **Random Forest** é o melhor modelo e é o usado para prever os novos clientes. As variáveis que mais pesam na decisão são a dívida total, o histórico de crédito, o mix de crédito, os juros dos empréstimos e os dias de atraso.

A diferença entre as duas linhas da tabela mostra por que a divisão por cliente importa. Cada cliente aparece em 8 meses com dados quase iguais. Na divisão por linha, o mesmo cliente cai no treino e no teste, e o modelo acerta parte do teste por "reconhecer" o cliente. Os ~64% da divisão por cliente são o desempenho esperado para clientes que o modelo nunca viu. O notebook mostra essa comparação.

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).
