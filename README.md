# Modelagem QSPR-DFT para Predição do Calor de Combustão
Este repositório reúne os scripts e notebooks desenvolvidos durante o mestrado para a construção e curadoria de banco de dados molecular, preparação de cálculos de DFT no Gaussian, extração automatizada de descritores eletrônicos, análise exploratória multivariada e treinamento de modelos de aprendizado de máquina para predição do calor de combustão (HC) de moléculas orgânicas.

O fluxo de trabalho integra descritores eletrônicos obtidos por DFT com técnicas estatísticas e modelos de regressão supervisionada, garantindo rastreabilidade metodológica, organização dos dados e reprodutibilidade computacional.

# Visão geral

O objetivo central deste projeto é investigar quais descritores eletrônicos obtidos por DFT podem ser mais relevantes para a predição do calor de combustão de moléculas orgânicas por meio de uma abordagem QSPR-DFT associada a aprendizado de máquina.

O repositório contempla principalmente:

- organização e padronização das moléculas do estudo
- recuperação de informações estruturais (nome IUPAC, SMILES, fórmula molecular, massa molecular)
- preparação de inputs para o Gaussian
- extração de descritores eletrônicos a partir de arquivos `.log`
- construção da base de dados final para modelagem
- análise exploratória dos dados
- PCA em 3D
- treinamento e validação de modelos de machine learning
- interpretabilidade via SHAP

# Contexto científico

Neste trabalho, foi desenvolvido um protocolo teórico-computacional para estimar o calor de combustão de moléculas orgânicas a partir de descritores eletrônicos obtidos via DFT. O conjunto principal utilizado na dissertação foi composto por 152 moléculas orgânicas distribuídas em diferentes classes químicas, com treinamento de modelos de regressão sob validação cruzada LOOCV e interpretabilidade via SHAP para o modelo representativo.

Os descritores extraídos incluem grandezas como:

- HOMO/LUMO e derivados
- gap eletrônico
- entalpia
- capacidade calorífica a volume constante
- momento de dipolo

Além dos descritores eletrônicos, foi avaliado o efeito da classe química como variável categórica codificada por one-hot encoding.
