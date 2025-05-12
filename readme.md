Grupo Pandas:
- Kleber
- Alisson
- Caique
- Carlos Eduardo
- Bruno



▪ COMO STARTAR O PROJETO: (comandos do terminal)
▪ cd C:/PASTA_QUE_ESTA_O_PROJETO/pandas
▪ pip install -r requirements.txt
▪ streamlit run dashboard.py

> Pandas: Manipulação e análise de dados tabulares (como tabelas do Excel), com funções para importar/exportar arquivos (CSV, Excel), limpar dados e calcular estatísticas.
> NumPy: Cálculos numéricos eficientes com arrays multidimensionais, base para operações matemáticas complexas em machine learning e ciência de dados.
> Matplotlib: Criação de gráficos estáticos (linhas, barras, dispersão) personalizáveis, ideal para visualizações básicas.
> Seaborn: Geração de gráficos estatísticos avançados (heatmaps, distribuições) com menos código, integrado ao Pandas.
> Streamlit: Construção rápida de web apps interativos para análise de dados e machine learning, sem necessidade de front-end complexo.

Cada uma complementa o fluxo de trabalho: Pandas/NumPy para processamento, Matplotlib/Seaborn para visualização, e Streamlit para compartilhar resultados.



*1 - Descrição do projeto e do seu contexto*

📊 Resumo das Funcionalidades do Dashboard de Notas Escolares
Importação de Dados: Leitura de planilhas com notas escolares.

Visualização de Distribuição: Histogramas por disciplina.

Análise de Correlação: Heatmap para verificar relações entre matérias.

Comparação entre Disciplinas: Gráfico de dispersão com nomes dos alunos e status (colorido).

Detecção de Outliers: Identificação de notas fora do padrão.

Preenchimento de Dados Faltantes: Por média ou mediana, conforme escolha.

Filtragem por Status: Exibe apenas alunos Aprovados, em Recuperação ou Reprovados.

Estatísticas Agrupadas: Médias e medianas por grupo (ex: Status).

Análise Comparativa: Comparação tabular entre o desempenho em diferentes disciplinas.

➡️ O sistema une gráficos e estatísticas para facilitar a interpretação do desempenho acadêmico.


*2 - Instruções claras de como executar o projeto (incluindo dependências e como instalar usando o pip, se necessário).*

- Instale o Python (caso ainda não tenha)
Baixe e instale o Python 3.9 ou superior:


-- Crie a seguinte estrutura de arquivos
Dentro da pasta do seu projeto (ex: analise_escolar), crie esta estrutura:

kotlin
Copiar
Editar
analise_escolar/
├── main.py                      ✅ Cria o Excel com os dados simulados
├── funcoes.py                   ✅ Contém as funções de análise
├── analise.py                   ✅ Arquivo que executa os gráficos e análises
└── data/
    └── raw/
        └── (vazio até rodar o main.py)


--- Abra o terminal na pasta do projeto e execute: pip install pandas numpy matplotlib seaborn fpdf openpyxl

Esses pacotes fazem:

pandas: leitura e manipulação de dados

numpy: cálculos matemáticos

matplotlib e seaborn: gráficos

fpdf: exportar PDF

openpyxl: salvar/ler .xlsx com o pandas


---- Execute os scripts em ordem

python main.py  
Isso criará o arquivo: data/raw/dados_simulados_turma.xlsx
Depois: execute a análise e gere gráficos + PDF 
python analise.py


----- Arquivos gerados
grafico_Matemática.png

grafico_História.png

heatmap_correlacao.png

comparacao_matematica_vs_historia.png

relatorio_graficos.pdf ✅ PDF final com tudo


*3 - Nome de todos os integrantes e a função de cada um no desenvolvimento.*

Caique - Product Owner (PO)

Kleber - Scrum Master

Alisson, Carlos, Bruno - Time de Desenvolvimento


*Questionário Obrigatório na Apresentação*

*1 - Como funciona o pip no Python e como ele foi utilizado no projeto?*

O pip é o gerenciador de pacotes oficial do Python, usado para instalar e gerenciar bibliotecas e dependências. 
Ao rodar o comando pip install <nome-do-pacote>, o pip busca o pacote na Python Package Index (PyPI) e o instala no ambiente de desenvolvimento.

*2 - Como foi feita a organização dos arquivos e pastas no projeto?*

Manipulação e visualização de dados simulados, com possível foco em previsão de desempenho acadêmico.

📁 Estrutura de Pastas e Arquivos:

Pasta/Arquivo - Função Principal

data/raw/ - Armazena dados brutos (ex: dados_simulados_turma.xlsx)

scripts/ - Scripts utilitários, como geração de dados (gerar_dados_teste.py)

src/ - Código-fonte principal dividido por módulos

└── tests/ - Testes unitários ou de integração

└── data_processing.py	- Limpeza e preparação de dados

dashboard.py - Interface interativa com Dash

.gitignore - Define o que o Git deve ignorar

readme.md - Explicação geral e instruções do projeto

requirements.txt - Lista de dependências Python

*3 - O que é arquitetura de software e como o grupo aplicou isso no projeto?*

Arquitetura de software é a forma como um sistema é organizado. No projeto, ela foi aplicada por meio da separação do código
em arquivos com funções específicas (main.py, analise.py e funcoes.py), o que facilita a leitura, manutenção e reutilização. 
Também houve organização de dados em pastas e uso de módulos para manter o código limpo e estruturado.
