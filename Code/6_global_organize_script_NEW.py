#________________________________________________________________________________________________________________________

#       ESTE SCRIPT ORGANIZA OS PARÂMETROS EXTRAÍDOS DOS OUTPUTS INSERIDOS NA PLANILHA global.xlsx EM COLUNAS SEPARADAS, PARA FACILITAR A VERIFICAÇÃO DOS DADOS
#______________________________________________________________________________________________________________________

#    CONVERTA PRIMEIRO O ARQUIVO global.csv PARA global.xlsx

### O que esse script faz: 1) Lê a planilha com dados verticais
###                        2) Extrai os dados na ordem: Dipole, HOMO, LUMO, GAP, Enthalpy, CV
###                        3) Organiza tudo em uma nova planilha.
#___________________________________________________________

import pandas as pd  

# Caminho do arquivo original 
file_path = "global.xlsx"

# Carrega o conteúdo da planilha
df = pd.read_excel(file_path, header=None)

# Lista para armazenar as linhas organizadas
organized_data = []

# Percorre o DataFrame em saltos de 3 linhas
i = 1
while i < len(df):

    # Linha i: nome da molécula
    molecule = df.iloc[i, 0]

    # Linha i+1: número de átomos
    n_atoms = df.iloc[i+1, 0]

    # Linha i+2: string com os valores
    values = df.iloc[i+2, 0]

    # Verifica se há dados válidos
    if pd.notna(molecule) and pd.notna(n_atoms) and pd.notna(values):
        try:
            Dipole, HOMO, LUMO, GAP, Enthalpy, CV = map(float, values.split(','))  

            # Adiciona à lista na ordem das colunas
            organized_data.append([
                molecule,              # Nome
                int(n_atoms),          # N_Atoms
                Dipole,                # Dipole (agora é a primeira coluna de dados)
                HOMO,                  # HOMO
                LUMO,                  # LUMO
                GAP,                   # GAP
                Enthalpy,              # Enthalpy
                CV                     # CV 
            ])
        except Exception as e:
            # Print opcional para debug, caso queira ver erros
            # print(f"Erro na linha {i}: {e}")
            pass

    # Avança 3 linhas para o próximo grupo
    i += 3

# Cria DataFrame com a nova ordem de colunas
# <-- CORREÇÃO AQUI: "Dipole" movido para o início das variáveis -->
df_final = pd.DataFrame(
    organized_data,
    columns=[
        "molecule", "N_Atoms", "Dipole (Debye)", "HOMO (Hartree)", "LUMO (Hartree)", "GAP (Hartree)",
        "enthalpy (Hartree)", "CV (Cal/mol.K)"])

# Define o nome do arquivo de saída
output_path = "parameters_global_organized.xlsx"

# Salva o DataFrame
df_final.to_excel(output_path, index=False)

print(f"Dados organizados e salvos em: {output_path}")