

# ESTE SCRIPT GERA SIGLAS A PARTIR DO NOME DAS MOLÉCULAS, A PARTIR DE UM RACIONAL QUE CRIA UMA ESTRUTURA XXXX000Y (X = CARACTERES DO NOME, Y = NÚMERO SEQUENCIAL)
# ELE ACESSA A PLANILHA 'MOLECULES.XLSX' NESTE DIRETÓRIO (Code/)
# ESTA ORGANIZAÇÃO TEM COMO OBJETIVO FACILITAR A IDENTIFICAÇÃO DAS MOLÉCULAS DO CONJUNTO DE DADOS

import re
import pandas as pd

def gerar_sigla_molecula(nome: str) -> str:
    """
    Gera uma sigla de 4 letras usando regras 'semânticas':
      - Divide por underscores, hífens, parênteses, etc.
      - Ignora tokens puramente numéricos.
      - 1 nome  -> (1ª letra + 2 do meio + última)
      - 2 nomes -> (2 primeiras do 1º + 2 primeiras do 2º)
      - 3 nomes -> (2 primeiras do 1º + 2 primeiras do 2º) ignora o 3º
      - 4 nomes -> (1ª letra de cada nome)
      - 5+ nomes -> pega 1ª letra de cada até completar 4
    Retorna a sigla em maiúsculo.
    """

    # 1. Substituir caracteres separadores por underscore
    #    (parênteses, chaves, colchetes, hífens, etc.)
    #    Assim fica fácil usar split abaixo.
    #    Exemplos: '(', ')', '[', ']', '{', '}', '-', etc.
    nome_limpo = re.sub(r"[()\[\]{}\-\(\),.]", "_", nome)

    # 2. Dividir por um ou mais underscores
    partes = re.split(r"_+", nome_limpo)

    # 3. Eliminar tokens puramente numéricos e espaços vazios
    palavras = []
    for p in partes:
        p = p.strip()
        if p.isdigit():
            # Se for só número, ignore
            continue
        if p:
            palavras.append(p)

    num = len(palavras)

    # Função auxiliar para remover qualquer caractere não alfabético
    def keep_only_letters(txt):
        return re.sub(r"[^a-zA-Z]", "", txt)

    if num == 0:
        # Caso nenhuma palavra sobrou (raro), devolve algo default
        return "XXXX"

    if num == 1:
        # 1 palavra -> 1ª + 2 do meio + última
        p = keep_only_letters(palavras[0])
        p = p.lower()  # processar em lower, depois sobe para upper
        L = len(p)
        # primeiramente, pega a primeira letra
        primeira = p[0]
        # "duas do meio" - vamos pegar as posições do meio
        meio1_idx = (L // 2) - 1
        meio2_idx = (L // 2)
        # ultima letra
        ultima = p[-1]
        sigla = f"{primeira}{p[meio1_idx]}{p[meio2_idx]}{ultima}"
        return sigla.upper()

    elif num == 2:
        # 2 palavras -> 2 primeiras letras de cada
        p1 = keep_only_letters(palavras[0]).lower()
        p2 = keep_only_letters(palavras[1]).lower()
        sigla = p1[:2] + p2[:2]
        return sigla.upper()

    elif num == 3:
        # 3 palavras -> 2 primeiras do 1º + 2 primeiras do 2º (ignora o 3º)
        p1 = keep_only_letters(palavras[0]).lower()
        p2 = keep_only_letters(palavras[1]).lower()
        sigla = p1[:2] + p2[:2]
        return sigla.upper()

    elif num == 4:
        # 4 palavras -> 1ª letra de cada
        p1 = keep_only_letters(palavras[0]).lower()
        p2 = keep_only_letters(palavras[1]).lower()
        p3 = keep_only_letters(palavras[2]).lower()
        p4 = keep_only_letters(palavras[3]).lower()
        sigla = p1[:1] + p2[:1] + p3[:1] + p4[:1]
        return sigla.upper()

    else:
        # 5 ou mais palavras -> 1ª letra de cada, até formar 4
        sigla_letras = []
        for p in palavras:
            p_limpo = keep_only_letters(p).lower()
            if p_limpo:
                sigla_letras.append(p_limpo[0])
                if len(sigla_letras) == 4:
                    break
        sigla = "".join(sigla_letras)
        return sigla.upper()


def gerar_siglas_excel(
    arquivo_excel: str = "MOLECULES.xlsx",
    aba: str = "PLANILHA1"
):
    """
    Lê a planilha 'PLANILHA1' de 'MOLECULES.xlsx', 
    onde a coluna A tem os nomes das moléculas.
    Gera a sigla (4 letras) e adiciona sufixo '-000X', 
    escrevendo o resultado na coluna B.
    Salva de volta no mesmo arquivo.
    """

    # Lê a planilha. Se não tiver cabeçalho, usar header=None
    # e acessar por df.iloc[:, 0] para a primeira coluna.
    # Aqui assumo que a planilha tem cabeçalho ou não? 
    # Se não tiver cabeçalho, usamos: header=None
    df = pd.read_excel(arquivo_excel, sheet_name=aba, header=None)

    # df.iloc[:,0] é a primeira coluna (coluna A) com os nomes
    nomes = df.iloc[:, 0].tolist()  # converte para lista

    siglas = []
    for i, nome_molecula in enumerate(nomes, start=1):
        if not isinstance(nome_molecula, str):
            # Caso haja células vazias ou com valores não-string, converte
            nome_molecula = str(nome_molecula)
        sigla_base = gerar_sigla_molecula(nome_molecula)
        # Monta o sufixo -000X
        sufixo = f"-{i:04d}"
        sigla_completa = sigla_base + sufixo
        siglas.append(sigla_completa)

    # Insere a lista de siglas na coluna B (df.iloc[:,1])
    # Se a planilha original só tiver 1 coluna, precisamos garantir 
    # que haja ao menos 2 colunas no DataFrame:
    if df.shape[1] == 1:
        # Se só tem 1 coluna, criamos a segunda
        df[1] = None

    df.iloc[:, 1] = siglas  # grava as siglas na coluna B

    # Salvar de volta no mesmo arquivo e mesma aba
    # Obs: index=False remove a coluna de índice
    # header=False não salva cabeçalho de colunas
    df.to_excel(arquivo_excel, sheet_name=aba, index=False, header=False)

def main():
    print("Iniciando script...")
    gerar_siglas_excel("MOLECULES.xlsx", "PLANILHA1")
    print("Siglas geradas e salvas com sucesso em 'MOLECULES.xlsx' (aba PLANILHA1).")

if __name__ == "__main__":
    main()
