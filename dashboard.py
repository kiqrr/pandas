import sys
import os

# Adiciona o caminho para localizar 'src'
sys.path.append(os.path.abspath("src"))

from data_processing import gerar_grafico
from data_processing import comparar_materias
from data_processing import gerar_relatorio_completo
from data_processing import detectar_valores_ausentes

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

# Adicionar após a seção de detecção de outliers
if st.button("Verificar Valores Ausentes"):
    # Verifica se há valores ausentes em todo o DataFrame
    valores_ausentes = df.isna().sum()
    colunas_com_ausentes = valores_ausentes[valores_ausentes > 0]
    
    if len(colunas_com_ausentes) > 0:
        st.write("Colunas com valores ausentes:")
        st.write(colunas_com_ausentes)
    else:
        st.success("Não foram encontrados valores ausentes no DataFrame!")

# Compare subjects
st.markdown("""
## Comparação entre Disciplinas

Este gráfico permite analisar a relação entre as notas dos alunos em duas disciplinas diferentes:

- **Cada ponto** representa um aluno (identificado pelo nome)
- **Cores**: verde = aprovado, laranja = recuperação, vermelho = reprovado
- **Linha diagonal tracejada**: representa desempenho igual nas duas matérias
- **Linha de tendência vermelha**: mostra a relação geral entre as notas
""")

materia1 = st.selectbox("Escolha a primeira matéria", df.columns[1:-1])
materia2 = st.selectbox("Escolha a segunda matéria", df.columns[1:-1])

if st.button("Comparar Matérias"):
    fig_comparacao = comparar_materias(df, materia1, materia2)
    st.pyplot(fig_comparacao)
    
    # Análise estatística automática
    correlacao = df[materia1].corr(df[materia2]).round(2)
    st.write(f"**Correlação entre as matérias:** {correlacao}")
    
    # Interpretação da correlação
    if correlacao > 0.7:
        st.success(f"Existe uma forte correlação positiva ({correlacao}) entre as notas destas disciplinas.")
    elif correlacao > 0.3:
        st.info(f"Existe uma correlação moderada ({correlacao}) entre as notas destas disciplinas.")
    else:
        st.warning(f"A correlação ({correlacao}) entre as disciplinas é fraca.")
        
    # Tabela comparativa
    st.subheader("Análise Comparativa")
    dados_comparacao = df[['Aluno', materia1, materia2, 'Status']]
    dados_comparacao['Diferença'] = (df[materia1] - df[materia2]).abs().round(1)
    st.dataframe(dados_comparacao.sort_values('Diferença', ascending=False))


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

# Adicionar seção de relatório completo
st.markdown("---")
st.header("Relatório Completo")
st.markdown("""
Esta funcionalidade gera um PDF com todas as análises dos dados:
- Resumo estatístico
- Gráficos de distribuição para cada matéria
- Análise de correlação entre disciplinas
- Estatísticas por status do aluno
- Outliers e pontos notáveis
- Conclusões
""")

if st.button("Gerar Relatório Completo"):
    with st.spinner("Gerando relatório... Aguarde um momento"):
        nome_arquivo = gerar_relatorio_completo(df)
        st.success(f"Relatório gerado com sucesso: {nome_arquivo}")
        
        # Opção de download
        with open(nome_arquivo, "rb") as file:
            st.download_button(
                label="Baixar Relatório PDF",
                data=file,
                file_name=nome_arquivo,
                mime="application/pdf"
            )