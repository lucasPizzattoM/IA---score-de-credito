import argparse
import json
from pathlib import Path

import joblib
from sklearn.metrics import accuracy_score, classification_report

from src.config import ARQUIVO_CLIENTES, ARQUIVO_METRICAS, ARQUIVO_MODELO
from src.modelo import carregar_dados, criar_modelos, dividir_por_cliente, separar_x_y


def main():
    parser = argparse.ArgumentParser(description="Treina a IA de score de crédito.")
    parser.add_argument("--dados", type=Path, default=ARQUIVO_CLIENTES, help="CSV com o histórico de clientes")
    parser.add_argument("--saida", type=Path, default=ARQUIVO_MODELO, help="Onde salvar o modelo treinado")
    args = parser.parse_args()

    tabela = carregar_dados(args.dados)
    x, y, grupos = separar_x_y(tabela)
    x_treino, x_teste, y_treino, y_teste = dividir_por_cliente(x, y, grupos)

    print(f"{len(tabela)} linhas de {grupos.nunique()} clientes")
    print(f"Treino: {len(x_treino)} linhas | Teste: {len(x_teste)} linhas\n")

    modelos = criar_modelos()
    acuracias = {}
    for nome, modelo in modelos.items():
        modelo.fit(x_treino, y_treino)
        acuracias[nome] = accuracy_score(y_teste, modelo.predict(x_teste))
        print(f"{nome}: {acuracias[nome]:.1%} de acerto")

    melhor = max(acuracias, key=acuracias.get)
    print(f"\nMelhor modelo: {melhor}\n")
    print(classification_report(y_teste, modelos[melhor].predict(x_teste)))

    # Depois de escolher, vc pode treinar o melhor modelo com todos os dados antes de salvar
    modelo_final = criar_modelos()[melhor]
    modelo_final.fit(x, y)

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo_final, args.saida)
    args.saida.with_name(ARQUIVO_METRICAS.name).write_text(
        json.dumps({"melhor_modelo": melhor, "acuracia_teste": acuracias}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Modelo salvo em {args.saida}")


if __name__ == "__main__":
    main()
