from data_processing import calcular_estatisticas
import pandas as pd

# test_analysis.py
def test_media_matematica():
    df = pd.read_excel("dados_simulados_turma.xlsx")
    assert calcular_estatisticas(df, "Matemática") == 7.64  # Valor esperado
