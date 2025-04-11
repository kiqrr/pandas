from src.data_processing import gerar_grafico
import pandas as pd
import streamlit as st  

st.title("Dashboard de Notas Escolares")
arquivo = st.file_uploader("Carregar planilha")
if arquivo:
    df = pd.read_excel(arquivo)
    st.dataframe(df)
    materia_selecionada = st.selectbox("Escolha a matéria", df.columns[1:-1])
    fig = gerar_grafico(df, materia_selecionada)
    st.pyplot(fig)

def carregar_dados_padrao():
    return pd.read_excel("dados_simulados_turma.xlsx")  # Dados pré-carregados para teste
