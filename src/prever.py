import argparse
from pathlib import Path

import joblib
import pandas as pd

from src.config import ARQUIVO_MODELO, ARQUIVO_NOVOS_CLIENTES, COLUNA_ALVO, COLUNA_ID


def prever(modelo, novos_clientes: pd.DataFrame) -> pd.Series:
    colunas_esperadas = list(modelo.feature_names_in_)
    faltando = set(colunas_esperadas) - set(novos_clientes.columns)
    
    if faltando:
        raise ValueError(f"Colunas faltando no arquivo de novos clientes: {sorted(faltando)}")

    x = novos_clientes[colunas_esperadas]
    return pd.Series(modelo.predict(x), index=novos_clientes.index, name="score_previsto")


def main():
    parser = argparse.ArgumentParser(description="Prevê o score de crédito de novos clientes.")
    parser.add_argument("arquivo", nargs="?", type=Path, default=ARQUIVO_NOVOS_CLIENTES,
                        help="CSV com os novos clientes")
    parser.add_argument("--modelo", type=Path, default=ARQUIVO_MODELO, help="Modelo salvo por src.treinar")
    parser.add_argument("--saida", type=Path, help="CSV para salvar as previsões (opcional)")
    args = parser.parse_args()

    if not args.modelo.exists():
        raise SystemExit(f"Modelo não encontrado em {args.modelo}. Rode antes: python -m src.treinar")

    modelo = joblib.load(args.modelo)
    novos = pd.read_csv(args.arquivo).drop(columns=[COLUNA_ID, COLUNA_ALVO], errors="ignore")

    novos["score_previsto"] = prever(modelo, novos)
    print(novos[["idade", "profissao", "salario_anual", "score_previsto"]].to_string())

    if args.saida:
        novos.to_csv(args.saida, index=False)
        print(f"\nPrevisões salvas em {args.saida}")


if __name__ == "__main__":
    main()
