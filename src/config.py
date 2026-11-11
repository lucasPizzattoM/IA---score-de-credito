"""Configurações do projeto: caminhos, colunas e parâmetros."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

PASTA_DADOS = RAIZ / "data"
PASTA_MODELOS = RAIZ / "models"

ARQUIVO_CLIENTES = PASTA_DADOS / "clientes.csv"
ARQUIVO_NOVOS_CLIENTES = PASTA_DADOS / "novos_clientes.csv"
ARQUIVO_MODELO = PASTA_MODELOS / "modelo_score.joblib"
ARQUIVO_METRICAS = PASTA_MODELOS / "metricas.json"

COLUNA_ALVO = "score_credito"
COLUNA_ID = "id_cliente"

#Colunas de texto que precisam virar números antes de entrar no modelo
#Conversao padrao para a leitura dessa IA
COLUNAS_CATEGORICAS = ["profissao", "mix_credito", "comportamento_pagamento"]

# 30% dos clientes ficam separados para o teste
PROPORCAO_TESTE = 0.3

# Semente fixa: o mesmo código sempre gera o mesmo resultado
SEMENTE = 42
