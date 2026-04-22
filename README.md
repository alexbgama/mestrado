# Modelagem QSPR-DFT para Predição do Calor de Combustão
Este repositório reúne os scripts e notebooks desenvolvidos durante o mestrado para a construção e curadoria de banco de dados molecular, preparação de cálculos de DFT no Gaussian, extração automatizada de descritores eletrônicos, análise exploratória multivariada e treinamento de modelos de aprendizado de máquina para predição do calor de combustão (HC) de moléculas orgânicas.

# Visão geral

O objetivo central deste projeto é investigar quais descritores eletrônicos obtidos por DFT podem ser mais relevantes para a predição do calor de combustão de moléculas orgânicas por meio de uma abordagem QSPR-DFT associada a aprendizado de máquina.

# Fluxo de trabalho

O fluxo de trabalho integra descritores eletrônicos obtidos por DFT com técnicas estatísticas e modelos de regressão supervisionada, garantindo rastreabilidade metodológica, organização dos dados e reprodutibilidade computacional:

## 1. Organização e padronização das moléculas do estudo

Objetivo

Organizar o conjunto de moléculas do estudo, atribuindo identificadores padronizados para uso ao longo de todo o pipeline.

2. Recuperação de informações estruturais
4. Preparação de inputs para o Gaussian
5. Extração de descritores eletrônicos a partir de arquivos `.log`
6. Construção da base de dados final para modelagem
7. Análise exploratória dos dados
8. PCA em 3D
9. Treinamento e validação de modelos de machine learning
10. Interpretabilidade via SHAP

# Contexto científico

Neste trabalho, foi desenvolvido um protocolo teórico-computacional para estimar o calor de combustão de moléculas orgânicas a partir de descritores eletrônicos obtidos via DFT. O conjunto principal utilizado na dissertação foi composto por 152 moléculas orgânicas distribuídas em diferentes classes químicas, com treinamento de modelos de regressão sob validação cruzada LOOCV e interpretabilidade via SHAP para o modelo representativo.

Os descritores extraídos incluem grandezas como:

- HOMO/LUMO e derivados
- gap eletrônico
- entalpia
- capacidade calorífica a volume constante
- momento de dipolo

Além dos descritores eletrônicos, foi avaliado o efeito da classe química como variável categórica codificada por one-hot encoding.
