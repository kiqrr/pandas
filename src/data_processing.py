import pandas as pd
import numpy as np
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
    Preenche valores faltantes em colunas numéricas usando o método especificado.
    """
    # Crie uma cópia do DataFrame para não modificar o original
    df_preenchido = df.copy()
    
    # Identifique colunas numéricas
    colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
    
    # Preencha valores faltantes em colunas numéricas
    if metodo == "media":
        for coluna in colunas_numericas:
            # Verifica se há valores NaN na coluna antes de preencher
            if df_preenchido[coluna].isna().any():
                df_preenchido[coluna] = df_preenchido[coluna].fillna(df[coluna].mean())
    elif metodo == "mediana":
        for coluna in colunas_numericas:
            if df_preenchido[coluna].isna().any():
                df_preenchido[coluna] = df_preenchido[coluna].fillna(df[coluna].median())
    
    # Para colunas não-numéricas (opcionalmente)
    colunas_texto = df.select_dtypes(include=['object']).columns
    for coluna in colunas_texto:
        # Preencher com o valor mais frequente (moda)
        if df_preenchido[coluna].isna().any():
            valor_mais_comum = df[coluna].mode()[0]
            df_preenchido[coluna] = df_preenchido[coluna].fillna(valor_mais_comum)
    
    return df_preenchido

def comparar_materias(df, materia1, materia2):
    """
    Gera gráficos comparativos entre duas matérias com análise estatística.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotagem com cores por status
    status_cores = {'Aprovado': 'green', 'Recuperação': 'orange', 'Reprovado': 'red'}
    cores = [status_cores.get(status, 'blue') for status in df['Status']]
    
    scatter = ax.scatter(df[materia1], df[materia2], alpha=0.7, c=cores)
    
    # Correção: Linha diagonal de referência
    lims = [
        min(ax.get_xlim()[0], ax.get_ylim()[0]),  # Pega valores escalares
        max(ax.get_xlim()[1], ax.get_ylim()[1])
    ]
    ax.plot([lims[0], lims[1]], [lims[0], lims[1]], 'k--', alpha=0.3, label="Desempenho igual")
    
    # Correção: Formatação da linha de tendência
    z = np.polyfit(df[materia1], df[materia2], 1)
    p = np.poly1d(z)
    ax.plot(df[materia1], p(df[materia1]), "r--", alpha=0.7, 
            label=f"Tendência (y={z[0]:.2f}x+{z[1]:.2f})")
    
    # Rotular os pontos com nomes dos alunos
    for i, aluno in enumerate(df["Aluno"]):
        ax.annotate(aluno, 
                   (df[materia1].iloc[i], df[materia2].iloc[i]),
                   fontsize=8,
                   xytext=(5, 5), 
                   textcoords='offset points')
    
    ax.set_xlabel(f"Notas em {materia1}")
    ax.set_ylabel(f"Notas em {materia2}")
    ax.set_title(f"Comparação de Notas: {materia1} vs {materia2}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
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