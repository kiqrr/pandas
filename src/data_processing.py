import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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