
: << 'COMENT'
# QSAR


 Este script shell automatiza a criação de arquivos de input para 
cálculos usando o Gaussian 16. Aqui está uma explicação detalhada do que o código faz:

## Funcionalidades Principais

- Itera sobre todos os arquivos .dat no diretório atual
- Cria novos arquivos de input com configurações específicas para o Gaussian
- Configura parâmetros importantes como:
    - Número de processadores (16)
    - Memória alocada (20GB)
    - Arquivo checkpoint (.chk)
- Define método de cálculo: M08HX/6-311++G** com correções de dispersão e solvatação

## Parâmetros de Cálculo

O script configura os seguintes parâmetros computacionais:

- Otimização de geometria (opt)
- Cálculo de frequências sem Raman (freq=noraman)
- Método DFT M08HX
- Base 6-311++G**
- Modelo de solvatação SMD
- Correção de dispersão empírica
- Controle SCF com ciclo máximo expandido

Ao final, o script cria um arquivo "[fila.sh](http://fila.sh)" contendo os comandos para
 executar todos os cálculos em sequência usando o Gaussian 16 (g16).

- O comando "dos2unix", adicionado na logo após o nome do arquivo de input, é para evitar 
problemas nos cálculos causados por eventuais caracteres especiais.

COMENT

################cria {input}s###################

for file in $(ls *.dat); do
			z="${file%.dat}"
            input=${z}
            echo "%nprocs=16" > ${input}".gjf"
            echo "%mem=20GB"      >> ${input}".gjf"
            echo "%chk="${input}".chk" >> ${input}".gjf" 
            echo "# opt freq=noraman  M08HX/6-311++G** scf=xqc SCRF=(SMD,Solvent=water) Empiricaldispersion=pfd Int(Grid=ultraFine) test" >> ${input}".gjf"
            echo " " >> ${input}".gjf"
            echo "${z}" >> ${input}".gjf"
            echo " " >> ${input}".gjf"
            cat ${z}.dat >> ${input}".gjf" 
			echo " " >> ${input}".gjf"
			echo " " >> ${input}".gjf"
            echo "g16 ${z}.gjf dos2unix" >> "fila.sh"            
done 

echo "inputs finalizados!!!"

###########################################################organiza area de calculo####################################################################################
	
exit