""" ler uma planilha Excel com nomes de substâncias (IUPAC e sinônimos), buscar os SMILES canônico e isomérico
a partir do PubChem e, em seguida, salvar essa informação em um novo arquivo Excel."""

# Importa a biblioteca 're' para dividir as strings de sinônimos com múltiplos separadores.
import re
# Importa tipos do módulo 'typing' para definir tipos opcionais e dicionários com tuplas.
from typing import Dict, Optional, Tuple

# Importa pandas para manipulação de planilhas e DataFrames.
import pandas as pd
# Importa pubchempy para consultar a base de dados do PubChem via Python.
import pubchempy as pcp
from tqdm import tqdm


def buscar_smiles_por_nome(
    nome: str, cache: Dict[str, Tuple[Optional[str], Optional[str]]]
) -> Tuple[Optional[str], Optional[str]]:
    """
    Esta função tenta obter o SMILES canônico e o isomérico de uma substância a partir de um nome dado (IUPAC ou sinônimo), utilizando o PubChemPy.

    - 'nome': a string do nome químico a ser pesquisado.
    - 'cache': um dicionário que armazena resultados de buscas anteriores para não consultar repetidas vezes o mesmo nome.

    Retorna uma tupla (SMILES_canônico, SMILES_isomérico), ambos podendo ser None.
    """

    # Verifica se o nome já foi consultado anteriormente no cache. Se sim, retorna diretamente o resultado armazenado.
    if nome in cache:
        return cache[nome]

    # Inicializa as variáveis de retorno com None.
    canonical_smiles: Optional[str] = None
    isomeric_smiles: Optional[str] = None

    try:
        # Tenta recuperar propriedades específicas do PubChem: "CanonicalSMILES", "IsomericSMILES", "ConnectivitySMILES"        # - "SMILES"
        # A chamada usa namespace="name", pois estamos pesquisando por nomes.
        props_list = pcp.get_properties(
            ["CanonicalSMILES", "IsomericSMILES", "ConnectivitySMILES", "SMILES"],
            nome,
            namespace="name",
        )
        # Se obteve algum resultado, pega o primeiro (props_list[0]) e extrai os campos.
        if props_list:
            props = props_list[0]
            # Atribui para canonical_smiles a primeira propriedade que existir na ordem:
            # CanonicalSMILES -> ConnectivitySMILES -> SMILES
            canonical_smiles = (
                props.get("CanonicalSMILES")
                or props.get("ConnectivitySMILES")
                or props.get("SMILES")
            )
            # Atribui para isomeric_smiles a propriedade IsomericSMILES, ou usa SMILES como fallback.
            isomeric_smiles = props.get("IsomericSMILES") or props.get("SMILES")
    except Exception:
        # Em caso de qualquer exceção, mantém canonical_smiles e isomeric_smiles como None.
        canonical_smiles = None
        isomeric_smiles = None

    # Armazena o resultado no cache para futuras consultas.
    cache[nome] = (canonical_smiles, isomeric_smiles)
    # Retorna a tupla com os SMILES (podem ser None).
    return canonical_smiles, isomeric_smiles


def processar_planilha(arquivo_entrada: str, arquivo_saida: str) -> None:
    """
    Lê a planilha, busca o SMILES para cada linha, add colunas com os resultados e salva em um novo Excel.
    Também exibe um resumo com a contagem de sucessos e falhas de buscas.    """

    # Lê o arquivo Excel usando o engine 'openpyxl' (necessário para .xlsx).
    df = pd.read_excel(arquivo_entrada, engine="openpyxl")
    # Cria as colunas onde serão armazenados os SMILES, inicializando com None.
    df["SMILES_canonical"] = None
    df["SMILES_isomeric"] = None

    # Inicializa o cache para evitar buscas repetidas ao PubChem.
    cache: Dict[str, Tuple[Optional[str], Optional[str]]] = {}
    # Inicializa contadores para as estatísticas finais:
    count_iupac = 0      # Quantas buscas retornaram SMILES via nome IUPAC.
    count_sinonimo = 0   # Quantas buscas retornaram SMILES via sinônimos.
    count_falha = 0      # Quantas buscas não retornaram nenhum SMILES.

    # Itera sobre cada linha do DataFrame (idx é o índice, linha é uma Series).
    for idx, linha in tqdm(df.iterrows(), total=len(df), desc="Processando"):    # barra de progresso
        # Obtém o valor do nome IUPAC, se existir.
        nome_iupac = linha.get("IUPAC_NAME")
        # Obtém a string de sinônimos, se existir.
        sinonimos = linha.get("Synonym")

        # Inicializa variáveis locais para armazenar os SMILES obtidos.
        smiles_canonico: Optional[str] = None
        smiles_isomerico: Optional[str] = None
        # Variável que indica se encontrou via 'iupac' ou 'sinonimo'.
        encontrado_por: Optional[str] = None

        # Primeiro, tenta buscar usando o nome IUPAC (se não for nulo ou vazio).
        if pd.notnull(nome_iupac) and str(nome_iupac).strip():
            # Convertendo para string e removendo espaços nas extremidades.
            nome_iupac_str = str(nome_iupac).strip()
            smiles_canonico, smiles_isomerico = buscar_smiles_por_nome(
                nome_iupac_str, cache
            )
            # Se ao menos um dos SMILES foi encontrado, registra 'iupac' no indicador.
            if smiles_canonico or smiles_isomerico:
                encontrado_por = "iupac"

        # Se não encontrou via IUPAC, tenta buscar via sinônimos.
        if not encontrado_por:
            # Verifica se a coluna de sinônimos não é nula nem vazia.
            if pd.notnull(sinonimos) and str(sinonimos).strip():
                # Divide a string de sinônimos em partes. Usa uma expressão regular
                # que considera: quebras de linha, vírgula, ponto e vírgula, barra vertical ou barra simples.
                partes = re.split(r"[\n,;|/]+", str(sinonimos))
                # Itera sobre cada sinônimo extraído.
                for sinonimo in partes:
                    # Remove espaços extras.
                    sinonimo = sinonimo.strip()
                    # Se a string estiver vazia, pula para o próximo.
                    if not sinonimo:
                        continue
                    # Tenta buscar SMILES para este sinônimo.
                    smiles_canonico, smiles_isomerico = buscar_smiles_por_nome(
                        sinonimo, cache
                    )
                    # Se encontrou, marca que foi via 'sinonimo' e interrompe o loop.
                    if smiles_canonico or smiles_isomerico:
                        encontrado_por = "sinonimo"
                        break

        # Atualiza os contadores conforme o resultado:
        if encontrado_por == "iupac":
            count_iupac += 1
        elif encontrado_por == "sinonimo":
            count_sinonimo += 1
        else:
            # Se não encontrou SMILES em nenhuma das tentativas.
            count_falha += 1

        # Preenche as colunas correspondentes no DataFrame.
        df.at[idx, "SMILES_canonical"] = smiles_canonico
        df.at[idx, "SMILES_isomeric"] = smiles_isomerico

    # Salva o DataFrame processado em um novo arquivo Excel.
    df.to_excel(arquivo_saida, index=False, engine="openpyxl")

    # Exibe resumo final da execução no console.
    total = len(df)
    print(f"Total de moléculas processadas: {total}")
    print(f"SMILES encontrados via IUPAC: {count_iupac}")
    print(f"SMILES encontrados via sinônimo: {count_sinonimo}")
    print(f"Falhas na busca de SMILES: {count_falha}")


if __name__ == "__main__":
    # Define os nomes dos arquivos de entrada e saída.
    ENTRADA = "iupac_smiles.xlsx"
    SAIDA = "smiles_output.xlsx"
    # Executa a função principal de processamento com esses arquivos.
    processar_planilha(ENTRADA, SAIDA)
