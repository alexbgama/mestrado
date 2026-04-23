# Modelagem QSPR-DFT para Predição do Calor de Combustão

Este repositório reúne os scripts e notebooks desenvolvidos durante o mestrado para a construção e curadoria de banco de dados molecular, preparação de cálculos de DFT no Gaussian, extração automatizada de descritores eletrônicos, análise exploratória multivariada e treinamento de modelos de aprendizado de máquina para predição do calor de combustão (HC) de moléculas orgânicas.

# Visão geral

O objetivo central deste projeto é investigar quais descritores eletrônicos obtidos por DFT podem ser mais relevantes para a predição de HC de moléculas orgânicas por meio de uma abordagem QSPR-DFT associada a aprendizado de máquina.

# Contexto científico

Neste trabalho, foi desenvolvido um protocolo teórico-computacional para estimar o calor de combustão de moléculas orgânicas a partir de descritores eletrônicos obtidos via DFT. O conjunto principal utilizado na dissertação foi composto por 152 moléculas orgânicas distribuídas em diferentes classes químicas, com treinamento de modelos de regressão sob validação cruzada LOOCV e interpretabilidade via SHAP para o modelo representativo.

Os descritores extraídos incluem grandezas como:

- HOMO/LUMO e derivados calculados
- gap eletrônico
- entalpia
- capacidade calorífica a volume constante
- momento de dipolo

Além dos descritores eletrônicos, foi avaliado o efeito da classe química como variável categórica codificada por one-hot encoding.

# Fluxo de trabalho

O fluxo de trabalho integra descritores eletrônicos obtidos por DFT com técnicas estatísticas e modelos de regressão supervisionada, garantindo rastreabilidade metodológica, organização dos dados e reprodutibilidade computacional:

### 1. Organização e padronização das moléculas do estudo

#### Objetivo

Organizar o conjunto de moléculas do estudo, atribuindo identificadores padronizados para uso ao longo de todo o pipeline.

#### Script principal

`2_gerar_siglas.py`

- Gera siglas ou identificadores curtos para as moléculas
- Padroniza a nomenclatura usada nos arquivos do trabalho
- Prepara a base para integração com os scripts seguintes

#### Entradas

Planilha com as moléculas originais.

#### Executar

`python 2_gerar_siglas.py`

#### Saídas

Tabela com identificadores moleculares padronizados.

#### Observações
Esta etapa é importante para garantir rastreabilidade entre nomes, estruturas, arquivos `.log` e tabelas finais.

### 2. Recuperação de informações estruturais

#### Objetivo

Obter representações estruturais confiáveis das moléculas, como nomes IUPAC e SMILES.

#### Script principal

`3_script_smiles.py`

- Consulta e organiza representações estruturais das moléculas
- Recupera ou valida SMILES
- Associa nomes estruturais à base do projeto

#### Entradas

Lista de moléculas padronizadas.

#### Executar

`python 3_script_smiles.py`

#### Saídas

Tabela contendo nomes IUPAC e SMILES.

#### Observações

Essa etapa é essencial para a curadoria da base de dados e para a posterior categorização química das moléculas.

### 3. Cálculo e validação de massa molecular

#### Objetivo

Calcular ou conferir massas moleculares das estruturas utilizadas no estudo.

#### Notebook principal

`4_SCRIPT_calculo_massa_molecular.ipynb`

- Lê as estruturas moleculares
- Calcula massas moleculares
- Compara resultados quando necessário com valores de referência

#### Entradas

Arquivo com SMILES ou estruturas moleculares.

#### Executar

Abrir o notebook e executar as células em sequência.

#### Saídas

Tabela com massas moleculares calculadas.

#### Observações

Essa etapa ajuda a conferir a consistência entre estrutura, fórmula e massa molecular antes do uso em modelagem.

### 4. Preparação dos inputs para cálculo de DFT

#### Objetivo

Automatizar a criação dos arquivos de entrada usados nos cálculos de estrutura eletrônica no Gaussian.

#### Script principal

`1_input_fila_water_creator.sh`

- Organiza estruturas para cálculo
- Prepara arquivos de entrada
- Padroniza o protocolo de submissão

#### Entradas

Estruturas moleculares previamente organizadas.

#### Executar

`bash 1_input_fila_water_creator.sh`

#### Saídas

Arquivos de entrada do Gaussian padronizados com número de procesadores, memória e cabeçalho de cálculo definidos.

#### Observações

Essa etapa integra a organização das estruturas moleculares ao início da etapa de cálculos teóricos.

### 5. Extração automatizada de descritores eletrônicos do DFT

#### Objetivo

Extrair os descritores eletrônicos e termodinâmicos obtidos via DFT e que serão utilizados na modelagem.

#### Script principal

`5_script_QSPR-DFT_values.bash`

- Percorre os arquivos `.log` do Gaussian
- Extrai propriedades eletrônicas e termodinâmicas
- Organiza esses valores em uma planilha `.csv`

Descritores extraídos incluem:

- HOMO
- LUMO
- gap eletrônico
- entalpia
- capacidade calorífica a volume constante
- momento de dipolo

#### Entradas

Arquivos `.log` do Gaussian.

#### Executar

`bash 5_script_QSPR-DFT_values.bash`

#### Saídas

Tabela contendo os descritores extraídos.

#### Observações

A planlha `.csv` gerada deve ser convertida para .xlsx para a etapa subsequente.

### 6. Organização dos descritores extraídos

#### Objetivo

Organizar os descritores extraídos na etapa 5 para integrá-los a base de dados a fim de calcular os parâmetros eletrônicos derivados do HOMO/LUMO.

#### Script principal

`6_global_organize_script_NEW.py`

- Separa os descritores extraídos em colunas rotuladas de acordo com cada descritor e sua unidade de medida

#### Entradas

Planilha `.xlsx` gerada na etapa anterior.

#### Executar

`python 6_global_organize_script_NEW.py`

#### Saídas

Planilha com descritores organizados em colunas.


### 7. Análise exploratória da propriedade-alvo e efeito das classes químicas

#### Objetivo

Investigar como o HC se distribui entre as classes químicas do conjunto de dados e verificar, com base em estatística descritiva e testes inferenciais, se há diferenças significativas entre essas classes.

#### Notebook principal

`7_exploring_HC_distribution.ipynb`

- Calcula estatísticas descritivas por classe, como número de amostras, média, mediana, desvio padrão, mínimo, máximo e amplitude de `HeatOfCombustion`
- Gera visualizações comparativas da distribuição do calor de combustão por classe, incluindo: boxplot, violin plot, gráficos de médias e contagens por classe
- Executa testes estatísticos para avaliar diferenças entre grupos: ANOVA de uma via, Kruskal-Wallis, comparações pareadas por Mann-Whitney para as classes mais frequentes.
- Decompõe a variância entre grupos e dentro dos grupos, calculando também o tamanho de efeito (eta-squared)
- Produz um resumo executivo com os principais resultados estatísticos

#### Entradas

Planilha `data_models.xlsx`.

#### Executar

Abrir o notebook e executar as células em sequência.

#### Saídas

- Estatísticas descritivas por classe
- Gráficos comparativos da distribuição de `HeatOfCombustion`
- Resultados de ANOVA, Kruskal-Wallis e testes pareados
- Estimativa da proporção de variância explicada pelas classes químicas

### 8. Análise exploratória: PCA em 3D

#### Objetivo

Explorar a organização do espaço químico por meio de PCA em três dimensões, usando um conjunto de descritores eletrônicos selecionados e classificando as classes das moléculas por SMARTS.

#### Notebook principal

`8_PCA_3D_work_features.ipynb`

- Define os descritores para a PCA: HOMO, GAP, CV (capacidade calorífica a volume constante), Enthalpy, DETmax (fração de transferência de elétrons)
- Compila e aplica uma hierarquia de padrões SMARTS para classificar as moléculas em classes químicas gerando uma classe final atribuída por prioridade
- Prepara a matriz numérica da PCA e padroniza os descritores com `StandardScaler`
- Calcula a variância explicada, os loadings e as equações lineares de PC1, PC2 e PC3 com base nos descritores padronizados
- Gera um gráfico PCA 3D colorido por classe química, heatmap dos loadings, agrupa classes pouco frequentes na categoria “outros”
- Exporta: tabela final de classificação SMARTS (`smarts_classificacao_final.xlsx`) e as figuras dos gráficos 

#### Entradas

`../database/data/data_models_v1.xlsx`

#### Executar

Abrir o notebook e executar as células em sequência.

#### Saídas

- PCA 3D
- Heatmap de loadings das três componentes principais
- Equações lineares das componentes principais
- Arquivo `.csv` com a classificação final por SMARTS
- Figuras em `.png` e `.svg`


### 9. Construção da base QSPR-DFT, treinamento dos modelos e interpretabilidade via SHAP

#### Objetivo

Construir a base final de modelagem a partir dos arquivos Gaussian, validar consistência estrutural, gerar descritores derivados, incorporar classes químicas por one-hot encoding, treinar modelos de regressão e interpretar o modelo representativo com SHAP.

#### Notebook principal

`9_main_v4_SHAP_Defesa.ipynb`

- Construção e validação da base de dados
- Preparação do alvo e seleção de descritores
- Classes químicas e codificação categórica
- Treinamento e avaliação dos modelos (sob validação cruzada LOOCV: Ridge, Lasso, ElasticNet, PLS, Random Forest, Gradient Boosting; métricas: R², Q², RMSE, MAE)
- Modelo representativo e interpretabilidade SHAP
- Gera: gráfico de importância global, beeswarm plot, ranking das variáveis mais relevantes e gráficos diagnósticos em HC para o modelo representativo)

#### Entradas

- Planilhas de base molecular
- Arquivos `.log` do Gaussian
- Base complementar com SMILES

#### Executar

Abrir o notebook e executar as células em sequência.

#### Saídas

- Base final consolidada para modelagem (`data_models.xlsx`, `model_performance.xlsx`)
- Descritores eletrônicos e derivados
- Classes químicas codificadas por one-hot
- Métricas de desempenho dos modelos
- Tabelas exportadas de base e performance
- Gráficos comparativos de modelagem
- Análise SHAP do modelo representativo
- Gráficos diagnósticos do modelo representativo
