
# ____________________________________________________________________________________________________________________

# ESTE SCRIPT EXTRAI OS PARÂMETROS ELETRÔNICOS E TERMOQUÍMICOS DO CÁLCULO DE DFT, PERCORRENDO CADA .LOG DENTRO DO DIRETÓRIO
# _________________________________________________________________________________________________________________________


echo "HOMO"	 > "saida.dat"                  # Cria (ou sobrescreve) o arquivo saida.dat contendo apenas o cabeçalho "HOMO"
echo "LUMO"	 >> "saida.dat"                 # Anexa ao final de saida.dat o cabeçalho "LUMO"
echo "GAP" >> "saida.dat"                   # Anexa ao final de saida.dat o cabeçalho "GAP"
echo "Enthalpy_Total"   >> "saida.dat"
echo "CV(Cal/mol.K)" >> "saida.dat"
echo "Dipole" >> "saida.dat"
# echo "S(Cal/mol.K)" >> "saida.dat"

 # Inicia um loop sobre cada código de molécula

#for x in DMXY0103	MEDI0134	DINP0099	DEXY0098	MADG0131	DSXE0105	DXOE0107	TOMD0163	DIYN0100	TEYN0162	DMXE0102	PAAC0139	SAAC0157	GCEL0118	PHPO0142	BRNL0092	DLML0101	ALTE0087	PPAL0148	EBUL0112	ENEL0113	FUCA0116	PHPL0141	HTAL0126	PLDE0144	CALE0093	BLDE0091	VILN0168	SCIC0159	GTAC0119	MLEC0135	PPAC0147	HTAC0125	PHAC0140	NTHC0138	PSUC0151	CPHC0097	CNAC0094	HROC0124	FURL0117	COBE0095	MLTE0137	ZMEO0169	DXYE0109	PYPE0152	AISE0083	PNEE0145	DXYB0108	ATHE0088	AIOE0082	MEBN0133	AARE0081	ALNA0085	HEYN0122	HEDI0121	PNTE0146	TRAN0166	SYRE0160	HXAE0128	HPTE0123	TPTE0164	HDEE0120	MLHE0136	DTRE0106	LFRE0130	ALDG0084	DXYL0110	DRHE0104	PROX0150	DYLE0111	EOXE0114	INOX0129	CPEE0096	TCYE0161	TRDE0167	FCHE0115	SCHE0158	QINE0153	TQUE0165	ALNQ0086	BENA0090	AAQE0080	PHRE0143	HTHE0127	AZAN0089	PPUN0149	RUAC0156	REQE0154	RFIE0155; do
DATA_DIR="../database/CP-QSAR-Gaussian_vacuum"
# O Bash irá percorrer todos os arquivos .log
for file in "$DATA_DIR"/*.log; do
    # Verifica se o arquivo existe (importante caso a pasta esteja vazia)
    [[ -e "$file" ]] || continue
    
    if [ -f "$file" ]; then

    # The processing
    echo "Processing: $file"

    # Strip the leading "./" and the ".log" suffix - this is the base name we'll reuse
    x="${file##*/}"
    x="${x%.log}"

    # Extrai o número de átomos da molécula
    nat=` awk '/NAtoms=/ {print $2}' ${x}".log" | tail -1`

    # Salva o número de átomos em um arquivo temp
    echo $nat > "nat_${x}.dat"  

    # Salva o nome da molécula em um arquivo temp
    echo $x > "nome_${x}.dat"

    # Extract the final dipole moment (Total dipole in Debye)
    dipole=$(awk '
      /Dipole moment \(field-independent basis, Debye\)/ {flag=1; next}
      flag && /Tot=/ {print $NF}
    ' ${x}.log | tail -1)

    echo $dipole > "dipole_${x}.dat"

    # Insert dipole moment into the final temporary file
    cat "dipole_${x}.dat" >> "final_${x}.dat"
    
    # Extrai as linhas que contêm os orbitais ocupados (HOMO) e virtuais (LUMO)
    awk /"Alpha  occ"/,/"Alpha virt"/ ${x}".log" | tail -2 > "hl_${x}.dat"

    # Do arquivo gerado, captura o último campo da primeira linha (valor de HOMO)
    head -1 "hl_${x}.dat" | awk '{ print $NF}' >> "homo_${x}.dat"

    # Insere o HOMO no arquivo final temporário da molécula
    cat "homo_${x}.dat" >> "final_${x}.dat"

    # Captura o quinto campo da segunda linha (valor de LUMO)
    tail -1 "hl_${x}.dat" | awk '{ print $5}' >>"lumo_${x}.dat"

    # Insere o LUMO no arquivo final temporário da molécula
    cat "lumo_${x}.dat" >> "final_${x}.dat"

    # Calcula o GAP (HOMO–LUMO) e anexa ao final do arquivo final da molécula
    paste -d' ' "homo_${x}.dat" "lumo_${x}.dat" | awk '{ print ( $1 - $2 ) }' >> "final_${x}.dat"

    # Extrai os parâmetros Enthalpy, CV e S:
    # Linha "Sum of...Enthalpies" = Valor total de H com correções térmicas  
    # Coluna 3 tabela = Capacidade calorífica (CV)
    # Coluna 4 tabela = Entropia (S)

    enthalpy=$(awk '/Sum of electronic and thermal Enthalpies/ {         # Encontra a linha exata
          print $NF;                                  					# Imprime o último campo (valor)
          exit                                      					# Interrompe após achar
        }
      ' ${x}.log)
      

    cv=$(awk '
      /^ *E \(Thermal\)/ { flag=1; next }
      flag && /^[[:space:]]*Total/ { print $3; exit }
    ' ${x}.log)

    # s=$(awk '
    #  /^ *E \(Thermal\)/ { flag=1; next }
    #  flag && /^[[:space:]]*Total/ { print $4; exit }
    #' ${x}.log)

    # Grava nos arquivos temporários

    echo $enthalpy > "enthalpy_${x}.dat"    					# Entalpia (Hartree)
    echo $cv > "cv_${x}.dat"									# Capacidade calorífica (Cal/mol.K)
    # echo $s > "s_${x}.dat"  									# Entropia (Cal/mol.K)

    # Insere os parâmetros no arquivo final temporário da molécula
    cat "enthalpy_${x}.dat" >> "final_${x}.dat"
    cat "cv_${x}.dat" >> "final_${x}.dat"
    # cat "s_${x}.dat" >> "final_${x}.dat"

    # Junta nome, número de átomos e os valores HOMO, LUMO, GAP, Enthalpy, CV e S (separando por vírgulas)
    paste -s -d',' "nome_${x}.dat" "nat_${x}.dat" "final_${x}.dat" >> "temp1.dat"

  fi
done

# Converte o cabeçalho inicial e os dados agregados em CSV
paste -s -d',' "saida.dat" > "global.csv" 

# Anexa todos os registros em temp1.dat ao arquivo global.csv
cat "temp1.dat" >> "global.csv" 

# Remove todos os arquivos .dat temporários
rm *.dat 
