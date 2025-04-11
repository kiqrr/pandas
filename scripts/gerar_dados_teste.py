import pandas as pd

# Dados fictícios
dados = {
    "Aluno": ["Ana", "Carlos", "Maria", "João", "Fernanda", "Pedro", "Juliana"],
    "Matemática": [8.5, 6.0, 9.2, 7.5, 8.0, 4.5, 9.8],
    "História": [7.0, 5.5, 8.8, 6.5, 7.5, 3.0, 9.0],
    "Ciências": [9.0, 6.5, 8.0, 7.0, 8.5, 5.0, 9.5],
    "Português": [8.0, 4.5, 9.0, 6.0, 8.5, 7.0, 9.2],
    "Geografia": [7.5, 3.8, 8.5, 5.5, 7.8, 6.5, 9.0],
    "Status": ["Aprovado", "Recuperação", "Aprovado", "Aprovado", "Aprovado", "Reprovado", "Aprovado"]
}

if __name__ == "__main__":  
    df = pd.DataFrame(dados)  
    df.to_excel("data/raw/dados_simulados_turma.xlsx", index=False)  