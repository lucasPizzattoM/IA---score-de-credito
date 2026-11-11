import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from src.config import COLUNA_ALVO, COLUNA_ID, COLUNAS_CATEGORICAS, PROPORCAO_TESTE, SEMENTE


def carregar_dados(caminho) -> pd.DataFrame:
    return pd.read_csv(caminho)


def separar_x_y(tabela: pd.DataFrame):
    #Separa as colunas de entrada(x), o alvo(y) e o id de cada cliente(grupos)
    y = tabela[COLUNA_ALVO]
    x = tabela.drop(columns=[COLUNA_ID, COLUNA_ALVO])
    grupos = tabela[COLUNA_ID]
    return x, y, grupos


def dividir_por_cliente(x, y, grupos):
    #Divide em treino e teste sem repetir clientes entre os dois
    #Cada cliente aparece em varios meses. Se a divisao for por linha, o mesmo cliente fica no treino e no teste
    #E a IA "aprende" o cliente em vez de aprender o padrao
  
    divisor = GroupShuffleSplit(n_splits=1, test_size=PROPORCAO_TESTE, random_state=SEMENTE)
    idx_treino, idx_teste = next(divisor.split(x, y, groups=grupos))
    return x.iloc[idx_treino], x.iloc[idx_teste], y.iloc[idx_treino], y.iloc[idx_teste]


def criar_modelos() -> dict[str, Pipeline]:
    #Monta os dois modelos como pipelines
    #Entao a conversão aprendida no treino e exatamente a mesma usada nos novos clientes(nao precisa refazer)
    
    #Random Forest: arvores nao precisam de escala, basta numerar as categorias
    preparo_floresta = ColumnTransformer(
        [
            (
                "categoricas",
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
                COLUNAS_CATEGORICAS,
            )
        ],
        remainder="passthrough",
        verbose_feature_names_out=False,
    )

    #KNN: mede as distancias, entao os numeros precisam estar na mesma escala
    #(senao o salario domina tudo) e as categorias viram colunas 0/1
    preparo_knn = ColumnTransformer(
        [
            ("categoricas", OneHotEncoder(handle_unknown="ignore"), COLUNAS_CATEGORICAS),
            ("numericas", StandardScaler(), make_column_selector(dtype_include="number")),
        ]
    )

    return {
        "Random Forest": Pipeline(
            [
                ("preparo", preparo_floresta),
                ("modelo", RandomForestClassifier(random_state=SEMENTE, n_jobs=-1)),
            ]
        ),
        "KNN": Pipeline(
            [
                ("preparo", preparo_knn),
                ("modelo", KNeighborsClassifier()),
            ]
        ),
    }
