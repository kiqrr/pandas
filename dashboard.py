import sys
import os

# Adiciona o caminho para localizar 'src'
sys.path.append(os.path.abspath("src"))

from data_processing import gerar_grafico

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF

st.title("Dashboard de Notas Escolares")

# File uploader
arquivo = st.file_uploader("Carregar planilha")

def carregar_dados_padrao():
    return pd.read_excel("data/raw/dados_simulados_turma.xlsx")  # Dados pré-carregados para teste

#def gerar_relatorio_eda(df):
#    profile = pandas_profiling.ProfileReport(df)
#    profile.to_file("relatorio_eda.html")
#    return "Relatório gerado: relatorio_eda.html"

def analisar_correlacao(df):
    correlacao = df.corr()
    return correlacao

def gerar_heatmap_correlacao(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
    return fig

def detectar_outliers(df, coluna):
    Q1 = df[coluna].quantile(0.25)
    Q3 = df[coluna].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[coluna] < Q1 - 1.5 * IQR) | (df[coluna] > Q3 + 1.5 * IQR)]
    return outliers

def exportar_graficos_pdf(graficos, nome_arquivo="relatorio_graficos.pdf"):
    pdf = FPDF()
    for grafico in graficos:
        pdf.add_page()
        pdf.image(grafico, x=10, y=10, w=180)
    pdf.output(nome_arquivo)
    return f"Relatório gerado: {nome_arquivo}"

def preencher_valores_faltantes(df, metodo="media"):
    if metodo == "media":
        return df.fillna(df.mean())
    elif metodo == "mediana":
        return df.fillna(df.median())

def comparar_materias(df, materia1, materia2):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df[materia1], df[materia2], alpha=0.7)
    ax.set_xlabel(materia1)
    ax.set_ylabel(materia2)
    ax.set_title(f"Comparação: {materia1} vs {materia2}")
    return fig

def filtrar_por_status(df, status):
    return df[df["Status"] == status]

def calcular_estatisticas_por_grupo(df, grupo, coluna):
    estatisticas = df.groupby(grupo)[coluna].agg(["mean", "median"])
    return estatisticas

if arquivo:
    df = pd.read_excel(arquivo)
else:
    df = carregar_dados_padrao()

st.dataframe(df)

# Select subject for analysis
materia_selecionada = st.selectbox("Escolha a matéria", df.columns[1:-1])
fig = gerar_grafico(df, materia_selecionada)
st.pyplot(fig)

# Generate correlation heatmap
if st.button("Gerar Heatmap de Correlação"):
    df_numerico = df.select_dtypes(include=['float64'])  # Filtra colunas numéricas
    fig_corr = gerar_heatmap_correlacao(df_numerico)
    st.pyplot(fig_corr)

# Detect outliers
coluna_outliers = st.selectbox("Escolha a coluna para detectar outliers", df.columns[1:-1])
if st.button("Detectar Outliers"):
    outliers = detectar_outliers(df, coluna_outliers)
    st.write(outliers)

# Fill missing values
metodo_preenchimento = st.selectbox("Escolha o método de preenchimento", ["media", "mediana"])
if st.button("Preencher Valores Faltantes"):
    df = preencher_valores_faltantes(df, metodo_preenchimento)
    st.dataframe(df)

# Compare subjects
materia1 = st.selectbox("Escolha a primeira matéria", df.columns[1:-1])
materia2 = st.selectbox("Escolha a segunda matéria", df.columns[1:-1])
if st.button("Comparar Matérias"):
    fig_comparacao = comparar_materias(df, materia1, materia2)
    st.pyplot(fig_comparacao)

# Filter by status
status_selecionado = st.selectbox("Filtrar por Status", ["Aprovado", "Reprovado", "Recuperação"])
if st.button("Filtrar por Status"):
    df_filtrado = filtrar_por_status(df, status_selecionado)
    st.dataframe(df_filtrado)

# Group statistics
grupo = st.selectbox("Escolha o grupo para calcular estatísticas", ["Status"])
coluna_grupo = st.selectbox("Escolha a coluna para calcular estatísticas", df.columns[1:-1])
if st.button("Calcular Estatísticas por Grupo"):
    estatisticas_grupo = calcular_estatisticas_por_grupo(df, grupo, coluna_grupo)
    st.write(estatisticas_grupo)
