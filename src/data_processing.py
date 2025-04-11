import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

def calcular_estatisticas(df, materia):
    media = df[materia].mean()
    mediana = df[materia].median()
    return {"Média": media, "Mediana": mediana}

def gerar_grafico(df, materia):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df[materia], kde=True, ax=ax)
    ax.set_title(f"Distribuição de Notas em {materia}")
    fig.savefig(f"grafico_{materia}.png")
    return fig

#import pandas_profiling
#def gerar_relatorio_eda(df):
#    """
#    Gera um relatório exploratório dos dados usando Pandas Profiling.
#    """
#    profile = pandas_profiling.ProfileReport(df)
#    profile.to_file("relatorio_eda.html")
#    return "Relatório gerado: relatorio_eda.html"

def analisar_correlacao(df):
    """
    Retorna a matriz de correlação entre as colunas numéricas.
    """
    correlacao = df.corr()
    return correlacao

def gerar_heatmap_correlacao(df):
    """
    Gera um heatmap da matriz de correlação.
    """
    # Filtra apenas colunas numéricas
    df_numerico = df.select_dtypes(include=['float64', 'int64'])
    
    # Remove valores NaN (se houver)
    df_numerico = df_numerico.dropna()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df_numerico.corr(), annot=True, cmap="coolwarm", ax=ax)
    return fig

def detectar_outliers(df, coluna):
    """
    Retorna os outliers de uma coluna usando o método IQR.
    """
    Q1 = df[coluna].quantile(0.25)
    Q3 = df[coluna].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[coluna] < Q1 - 1.5 * IQR) | (df[coluna] > Q3 + 1.5 * IQR)]
    return outliers

def exportar_graficos_pdf(graficos, nome_arquivo="relatorio_graficos.pdf"):
    """
    Exporta uma lista de gráficos como um relatório PDF.
    """
    pdf = FPDF()
    
    for grafico in graficos:
        pdf.add_page()
        pdf.image(grafico, x=10, y=10, w=180)
    
    pdf.output(nome_arquivo)
    return f"Relatório gerado: {nome_arquivo}"

def preencher_valores_faltantes(df, metodo="media"):
    """
    Preenche valores faltantes em todas as colunas numéricas usando o método especificado.
    """
    if metodo == "media":
        return df.fillna(df.mean())
    elif metodo == "mediana":
        return df.fillna(df.median())

def comparar_materias(df, materia1, materia2):
    """
    Gera gráficos comparativos entre duas matérias.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.scatter(df[materia1], df[materia2], alpha=0.7)
    
    ax.set_xlabel(materia1)
    ax.set_ylabel(materia2)
    
    ax.set_title(f"Comparação: {materia1} vs {materia2}")
    
    return fig

def filtrar_por_status(df, status):
    """
    Filtra o DataFrame por status específico.
    """
    return df[df["Status"] == status]

def calcular_estatisticas_por_grupo(df, grupo, coluna):
    """
    Calcula estatísticas (média e mediana) agrupadas por uma categoria.
    """
    estatisticas = df.groupby(grupo)[coluna].agg(["mean", "median"])
    return estatisticas