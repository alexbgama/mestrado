
# Buscar correspondência entre o nome original das moléculas dos datasets do DFT e do NIST





import pandas as pd
from thefuzz import process, fuzz

def correlacao_aproximada(
    arquivo_menor='bd-menor.xlsx', 
    arquivo_maior='bd-maior.xlsx', 
    coluna_nome_menor='NAME-MENOR', 
    coluna_nome_maior='NAME-MAIOR', 
    corte_score=50
):
    """
    Cruza dois DataFrames buscando o nome mais parecido.
    corte_score: Nota mínima (0-100) para aceitar a sugestão.
    """
    
    # 1. Carregar os dados
    df_menor = pd.read_excel(arquivo_menor)
    df_maior = pd.read_excel(arquivo_maior)
    
    # Garantir que são strings
    df_menor[coluna_nome_menor] = df_menor[coluna_nome_menor].astype(str)
    lista_nomes_maior = df_maior[coluna_nome_maior].astype(str).tolist()
    
    # Listas para armazenar resultados
    melhores_matches = []
    scores = []
    
    print("Iniciando correspondência difusa (Fuzzy Matching)...")
    
    # 2. Iterar sobre cada nome da lista MENOR
    total = len(df_menor)
    for i, nome_busca in enumerate(df_menor[coluna_nome_menor]):
        if i % 100 == 0: print(f"Processando {i}/{total}...")
        
        # process.extractOne acha o melhor candidato na lista maior
        # scorer=fuzz.token_sort_ratio é bom para palavras fora de ordem ou pontuação
        match, score = process.extractOne(
            nome_busca, 
            lista_nomes_maior, 
            scorer=fuzz.token_sort_ratio
        )
        
        if score >= corte_score:
            melhores_matches.append(match)
            scores.append(score)
        else:
            melhores_matches.append(None) # Não achou nada confiável
            scores.append(score)
            
    # 3. Adicionar resultados no DataFrame menor
    df_menor['Nome_Encontrado_Maior'] = melhores_matches
    df_menor['Score_Similaridade'] = scores
    
    # Opcional: Trazer dados da tabela maior (como um PROCV)
    # Fazemos um merge (join) usando o nome encontrado
    df_final = pd.merge(
        df_menor, 
        df_maior, 
        left_on='Nome_Encontrado_Maior', 
        right_on=coluna_nome_maior, 
        how='left',
        suffixes=('_menor', '_maior')
    )
    
    # Salvar
    df_final.to_excel("RESULTADO_CORRELACAO.xlsx", index=False)
    print("Concluído! Arquivo 'RESULTADO_CORRELACAO.xlsx' gerado.")

# --- Execução ---
# Substitua pelos nomes reais dos seus arquivos e colunas
correlacao_aproximada('bd-menor.xlsx', 'bd-maior.xlsx')