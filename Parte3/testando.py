
HEXA = "0x04400001"

tipoR = {"100000":"add", "100010":"sub",
"101010":"slt", "100100":"and", "100101":"or", "100110":"xor",
"100111":"nor", "010000":"mfhi", "010010":"mflo", "100001":"addu",
"100011":"subu", "011000":"mult", "011001":"multu", "011010":"div",
"011011":"divu", "000000":"sll", "000010":"srl", "000011":"sra",
"000100":"sllv", "000110":"srlv", "000111":"srav", "001000":"jr"}

tipoIJ = {"001111":"lui", "001000":"addi", "001010":"slti",
"001100":"andi", "001101":"ori", "001110":"xori", "100011":"lw",
"101011":"sw", "000001":"bltz", "000100":"beq", "000101":"bne",
"001001":"addiu", "100000":"lb", "100100":"lbu", "101000":"sb",
"000010":"j", "000011":"jal"}

# dicionario com todos os registradores
registradores = {"$0":"0",  "$1":"0",  "$2":"0",  "$3":"0",  "$4":"0",
"$5":"0",  "$6":"0",  "$7":"0",  "$8":"0",  "$9":"0",  "$10":"0",
"$11":"0",  "$12":"0",  "$13":"0",  "$14":"0",  "$15":"0",  "$16":"0",
"$17":"0",  "$18":"0",  "$19":"0",  "$20":"0",  "$21":"0",  "$22":"0",
"$23":"0",  "$24":"0",  "$25":"0",  "$26":"0",  "$27":"0",  "$28":"0",
"$29":"0",  "$30":"0",  "$31":"0"}

memoria = {}


def main():
    '''binario = converteParaBinario(HEXA) # converte o hexadecimal recebido para binario
    tipo = defineTipo(binario) # pega o tipo de codigo do hexadecimal(r, i, j, s)
    print( escreveCodigo(binario, tipo) ) # escreve o codigo na tela'''
    #print(devolveRegistradores())
    with open("entrada2.txt") as entrada, open("saida2.txt", 'w') as saida:
        comandos = []
        for linha in entrada.readlines():
            comandos.append(linha)
        
        i = 0
        cont = 0
        while i < len(comandos) and cont < 15:
            binario = converteParaBinario(comandos[i]) # converte o hexadecimal da linha para binario
            tipo = defineTipo(binario) # pega o tipo de codigo do hexadecimal(r, i, j, s)
            comando_atual = escreveCodigo(binario, tipo, executar = True)
            if ('j ' in comando_atual) or ('jal ' in comando_atual) or ('beq ' in comando_atual) or ('bne ' in comando_atual) or ('bltz ' in comando_atual) or ('jr ' in comando_atual):
                i = operacaoDePulo(comando_atual, i)
            else: i += 1
            cont += 1
            
            '''print(comando_atual)
            print(comando_atual, file = saida) # escreve o codigo no arquivo de saida
            print(devolveRegistradores(), file = saida)'''
            

def converteParaBinario(hexa):
    base = 16
    bits = 8

    binario = bin(int(hexa, base))[2:].zfill(bits)
    binario = str(binario)

    binario = ('0' * (32 - len(binario))) + binario

    return binario

def decimalParaBinario(num):
    if num >= 0:
        return bin(num)[2:]
    else:
        return '1' + bin(2147483648 + num)[2:]

def binarioParaDecimal(binario):
    decimal = str(int(binario, 2)) if len(binario) < 32 or binario[0] != '1' else str(int(binario[1:], 2) - 2147483648)
    return decimal

def armazenaRegistradores(registrador, binario):
    registradores[registrador] = binarioParaDecimal(binario)

def defineTipo(binario): # devolve um char com o tipo de operação do hexadecimal(r, i, j, s)
    tipo = "rs"
    for i in range(6): # analiza os seis primeiros digitos do numero binario
        if binario[i] == '1': # caso haja algum '1' no numero binario
            tipo = "ij" # tip passa a ser 'ij'
            break # sai do laco

    if tipo == "rs": # caso tipo continue sendo "rs"(nao achou nenhum 1 nos seis primeiros digitos)
        if binario[26:] == "001100": # analiza o func, e caso seja igual a "001100"(syscall)
            return 's'
        return 'r'# caso nao seja tipo 's'
    return 'ij'# caso nao seja nem 's' nem 'r'

def escreveCodigo(binario, tipo, executar = False):
    codigo = ''

    if tipo == 's': # caso o comando seja do tipo 's'
        codigo = "syscall"


    elif tipo == 'r': # caso o comando seja do tipo r
        func = tipoR[ binario[26:] ] # procura no dicionario tipoR, do 26º digito pra frente, a que comando o binario se refere

        if func == "jr": # caso o func seja 'jr'
            registrador = str(int(binario[6:11], 2)) # registrador vai ser igual a sequencia binaria, do sexto bit ao decimo, na base 10
            codigo = func + ' $' + registrador # codigo = 'jr' + $registrador
        elif func in ("mfhi", "mflo"): # caso o func seja "mfhi" ou "mflo"
            registrador = str(int(binario[16:21], 2))
            codigo = func + ' $' + registrador
        elif func in ("mult", "multu", "div", "divu"): # caso o func seja um desses
            registrador1, registrador2 = str(int(binario[6:11], 2)), str(int(binario[11:16], 2))
            codigo = func + ' $' + registrador1 + ', $' + registrador2
        elif func in ("sll", "srl", "sra"): # caso o func seja um desses
            registrador1, registrador2, numero = str(int(binario[16:21], 2)), str(int(binario[11:16], 2)), int(binario[21:26], 2)
            codigo = func + ' $' + registrador1 + ', $' + registrador2 + ', ' + str(numero)
            executaComandos(func, executar, registrador1 = '$' + registrador1, registrador2 = '$' + registrador2, numero = numero)
        elif func in ("sllv", "srlv", "srav"): # caso o func seja um desses
            registrador1, registrador2, registrador3 = str(int(binario[16:21], 2)), str(int(binario[11:16], 2)), str(int(binario[6:11], 2))
            codigo = func + ' $' + registrador1 + ', $' + registrador2 + ', $' + registrador3
            executaComandos(func, executar, registrador1 = '$' + registrador1, registrador2 = '$' + registrador2, registrado3 = '$' + registrador3)
        else: # caso o func nao seja nenhum dos acima (ou seja, func eh dos que usam tres registradores, como 'add' ou 'sub')
            registrador1, registrador2, registrador3 = str(int(binario[16:21], 2)), str(int(binario[6:11], 2)), str(int(binario[11:16], 2))
            codigo = func + ' $' + registrador1 + ', $' + registrador2 + ', $' + registrador3
            executaComandos(func, executar, registrador1 = '$' + registrador1, registrador2 = '$' + registrador2, registrador3 = '$' + registrador3)

    elif tipo == 'ij': # caso o comando seja do tipo 'i' ou 'j'
        func = tipoIJ[ binario[:6] ]

        if func == "lui": # caso o func seja 'lui'
            registrador, numero = str(int(binario[11:16], 2)), int(binario[16:32], 2) # registrador eh igual a sequencia binaria do 11 bit ao 16 bit. numero vai ser o resto da sequencia binaria
            codigo = func + ' $' + registrador + ', ' + str(numero)
            executaComandos(func, executar, registrador1 = '$' + registrador, numero = numero)
        elif func == "bltz": # caso o func seja 'bltz'
            registrador, numero = str(int(binario[6:11], 2)), int(binario[17:32], 2)
            numero = numero - 32768 if binario[16] == '1' else numero
            codigo = func + ' $' + registrador + ', ' + str(numero)
        elif func in ("addi", "slti", "andi", "ori", "xori", "addiu"): # se func for um desses
            registrador1, registrador2, numero = str(int(binario[11:16], 2)), str(int(binario[6:11], 2)), int(binario[17:32], 2) # dessa vez ele conta do 17 bit ao fim, pois o 16 vai servir pra checar se o numero eh negativo
            numero = numero - 32768 if binario[16] == '1' else numero # caso o numero seja negativo, ele vai ser: numero - 32768. mais em https://www.youtube.com/watch?v=ZwRfnmXY7VY
            codigo = func + ' $' + registrador1 + ', $' + registrador2 + ', ' + str(numero)
            executaComandos(func, executar, registrador1 = '$' + registrador1, registrador2 = '$' + registrador2, numero = numero)
        elif func in ("lw", "sw", "lb", "lbu", "sb"):
            registrador1, registrador2, numero = str(int(binario[11:16], 2)), str(int(binario[6:11], 2)), int(binario[17:32], 2) # dessa vez ele conta do 17 bit ao fim, pois o 16 vai servir pra checar se o numero eh negativo
            numero = numero - 32768 if binario[16] == '1' else numero # caso o numero seja negativo, ele vai ser: numero - 32768. mais em https://www.youtube.com/watch?v=ZwRfnmXY7VY
            codigo = func + ' $' + registrador1 + ', ' + str(numero) + '($' + registrador2 + ')'
            executaComandos(func, executar, registrador1 = '$' + registrador1, registrador2 = '$' + registrador2, numero = numero)
        elif func in ("beq", "bne"):
            registrador1, registrador2, numero = str(int(binario[6:11], 2)), str(int(binario[11:16], 2)), int(binario[17:32], 2)
            numero = numero - 32768 if binario[16] == '1' else numero
            codigo = func + ' $' + registrador1 + ', $' + registrador2 + ', ' + str(numero)
        elif func in ("j", "jal"):
            numero = int(binario[12:32], 2)
            codigo = func + ' ' + str(numero)

    return codigo

def executaComandos(func, executar, registrador1 = '', registrador2 = '', registrador3 = '', numero = None):
    if executar:
        operacaoAritmetica(func, registrador1, registrador2, registrador3, numero)
        operacaoLogica(func, registrador1, registrador2, registrador3, numero)
        instrucoesDeMemoria(func, registrador1, registrador2, numero)
        
    
###########################################################################################################################################
#funcao que vai realizar a operacao aritmetica especificada pelo codigo e armazenar o resultado nos registradores especificos
def operacaoAritmetica(func, registrador1, registrador2, registrador3, numero):
    if registrador2 != '':
        binReg2 = decimalParaBinario( int(registradores[registrador2]) )

    if registrador3 != '':
        binReg3 = decimalParaBinario( int(registradores[registrador3]) )
        pulo = int( registradores[registrador3] )

    if numero != None:
        binNumero = decimalParaBinario( numero )

    
    if func == "add":
        registradores[registrador1] = str( int(registradores[registrador2]) + int(registradores[registrador3]))
        
    if func == "sub":
        registradores[registrador1] = str( int(registradores[registrador2]) - int(registradores[registrador3]))
        
    if func == "addi":
        registradores[registrador1] = str( int(registradores[registrador2]) + numero)

    if func == "addu":
        registradores[registrador1] = str(int(registradores[registrador2]) + int(registradores[registrador3]))

    if func == "subu":
        registradores[registrador1] = str(int(registradores[registrador2]) - int(registradores[registrador3]))

    if func == "addiu":
        registradores[registrador1] = str(int(registradores[registrador2]) + numero)

    if func == "lui":
        binNumero = binNumero + ( '0' * 16 ) # adiciona 16 zeros a direita do binario do numero recebido
        registradores[registrador1] = binarioParaDecimal(binNumero) # armazena o resultado no registrador

    if func == "sll": # move o valor binario do registrador 2 um certo numero de vezez (numero) para a esquerda e armazena o resultado no registrador 1
        binSSL = instrucaoSLL(binReg2, numero)
        armazenaRegistradores(registrador1, binSSL)

    if func == "srl": # move o valor binario do registrador 2 um certo numero de vezez (numero) para a direita e armazena o resultado no registrador 1
        binSRL = instrucaoSRL(binReg2, numero)
        armazenaRegistradores(registrador1, binSRL)

    if func == "sra": # mesma coisa do srl, porem preenche com 0 ou com 1 dependendo do sinal do numero passado
        binSRA = instrucaoSRA(binReg2, numero)
        armazenaRegistradores(registrador1, binSRA)

    # fazem o mesmo que as instrucoes de cima, porem ao inves de receberem um numero direto da instrucao
    # recebem o registrador que o numero vai estar. isso faz com que seja preciso lidar com casos em que o numero no
    # registrador seja maior que 32 ou menor que 0
    if func == "sllv":
        binSLLV = instrucaoSLL( binReg2, (pulo % 32) )
        armazenaRegistradores(registrador1, binSLLV)

    if func == "srlv":
        binSRLV = instrucaoSRL(binReg2, (pulo % 32))
        armazenaRegistradores(registrador1, binSRLV)

    if func == "srav":
        binSRAV = instrucaoSRA(binReg2, (pulo % 32))
        armazenaRegistradores(registrador1, binSRAV)


# funcao que recebe o primeiro registrador e os demais dados(se necessario), e realiza as operacoes logicas acesseando e armazenando
# em registradores
def operacaoLogica(func, registrador1, registrador2, registrador3, numero):
    # caso seja uma operacao que mecha com os 3 registradores
    if registrador2 != '' and registrador3 != '':
        # cria duas variaveis que recebem o valor contido no segundo e terceiro registradores especificados
        binReg2, binReg3 = decimalParaBinario( int(registradores[registrador2]) ), decimalParaBinario( int(registradores[registrador3]) )
        maior = max( len(binReg2), len(binReg3) )  # maior eh uma variavel que recebe o tamanho do maior registrador
        # completa o tamanho do menor registrador com 0 ateh o tamanho do maior registrador
        # ex. '1000', '10' = '1000', '0010'
        binReg2, binReg3 = ('0' * (maior - len(binReg2))) + binReg2, ('0' * (maior - len(binReg3))) + binReg3

    # caso seja uma operacao que mecha com 2 registradores e um inteiro
    elif registrador2 != '' and numero != None:
        # cria duas variaveis que recebem o valor contido no segundo registrador e o numero que foi passado
        binReg2, binNum = decimalParaBinario(int(registradores[registrador2])), decimalParaBinario( numero )
        maior = max(len(binReg2), len(binNum))  # maior eh uma variavel que recebe o tamanho do maior registrador.
        # vvv completa o tamanho do menor registrador com 0 ateh o tamanho do maior registrador vvv
        # vvv ex. '1000', '10' = '1000', '0010' vvv
        binReg2, binNum = ('0' * (maior - len(binReg2))) + binReg2, ('0' * (maior - len(binNum))) + binNum


    if func == "and": # and bit a bit
        andBaB = instrucaoAnd(binReg2, binReg3)
        armazenaRegistradores(registrador1, andBaB)

    if func == "or": # or bit a bit
        orBaB = instrucaoOr(binReg2, binReg3)
        armazenaRegistradores(registrador1, orBaB)

    if func == "xor": # xor bit a bit (bit != bit => 1  /  bit == bit => 0)

        xorBaB = instrucaoXor(binReg2, binReg3)
        armazenaRegistradores(registrador1, xorBaB)

    if func == "nor": # nor bit a bit (not or)
        norBaB = instrucaoNor(binReg2, binReg3)
        armazenaRegistradores(registrador1, norBaB)

    if func == "andi": 
        andiBaB = instrucaoAnd(binReg2, binNum)
        armazenaRegistradores(registrador1, andiBaB)

    if func == "ori":
        oriBaB = instrucaoOr(binReg2, binNum)
        armazenaRegistradores(registrador1, oriBaB)

    if func == "xori":
        xoriBaB = instrucaoXor(binReg2, binNum)
        armazenaRegistradores(registrador1, xoriBaB)


def operacaoDePulo(expressao, posicao):
    if ('j ' or 'jal ') in expressao:
        pulo = int( expressao.split()[1] )
        posicao = pulo
    elif ('bne ') in expressao:
        reg1 = expressao.split()[1].strip(',')
        reg2 = expressao.split()[2].strip(',')
        pulo = int( expressao.split()[3] ) + 1
        if registradores[reg1] != registradores[reg2]:
            posicao = posicao + pulo
        else: posicao += 1
    elif ('beq ') in expressao:
        reg1 = expressao.split()[1].strip(',')
        reg2 = expressao.split()[2].strip(',')
        pulo = int( expressao.split()[3] ) + 1
        if registradores[reg1] == registradores[reg2]:
            posicao = posicao + pulo
        else: posicao += 1
    elif ('bltz ') in expressao:
        reg = expressao.split()[1].strip(',')
        pulo = int( expressao.split()[2] ) + 1
        if int(registradores[reg]) < 0:
            posicao = posicao + pulo
        else: posicao += 1
        
    return posicao


def instrucoesDeMemoria(func, registrador1, registrador2, pulo):
    endereco = int( registradores[registrador2] ) + (pulo // 4) # cada endereco vai de 4 em quatro bytes (8 * 4 = 32)
    conteudo = int(registradores[registrador1]) # conteudo que pode ser armazenado em algum endereco de memoria
    pulo = pulo % 4

    if func == "sw" and pulo == 0: # caso a funcao seja 'sw'(store word)
        print(func, registrador1, registrador2)
        memoria[endereco] = bin(conteudo)[2:] # memoria recebe, ou modifica, um endereco de memoria com o valor binario do conteudo

    if func == "lw" and pulo == 0: # caso seja a funcao seja 'lw'
        print(func, registrador1, registrador2)
        conteudo = memoria[endereco] if (endereco in memoria) else '0' # carrega o registrador1 com o valor contido no endereco
        armazenaRegistradores(registrador1, conteudo)
    if func == "sb":
        print(func, registrador1, registrador2)
        binarioMemoria = memoria[endereco] # variavel que recebe o conteudo armazenado naquele endereco de memoria
        binarioMemoria = ( 32 - len(binarioMemoria) ) * '0' + binarioMemoria
        conteudo = bin( int(registradores[registrador1]) )[2:]
        conteudo = conteudo[-8:]
        conteudo = ( (8 - len(conteudo)) * '0') + conteudo
        binarioFinal = binarioMemoria[:32 - (8 * (pulo + 1))] + conteudo + binarioMemoria[32 - (8 * pulo):]
        memoria[endereco] = binarioFinal[binarioFinal.find('1'):]
    if func == "lb":
        print(func, registrador1, registrador2)
        binarioMemoria = memoria[endereco] # variavel que recebe o conteudo armazenado naquele endereco de memoria
        binarioMemoria = ((32 - len(binarioMemoria)) * '0') + binarioMemoria
        binarioMemoria = binarioMemoria[32 - (8 * (pulo+1)) : 32 - (8 * pulo)]
        binarioFinal = (24 * '1') + binarioMemoria if binarioMemoria[0] == '1' else binarioMemoria
        armazenaRegistradores(registrador1, binarioFinal)
    if func == "lbu":
        print(func, registrador1, registrador2)
        binarioMemoria = memoria[endereco] # variavel que recebe o conteudo armazenado naquele endereco de memoria
        binarioMemoria = ((32 - len(binarioMemoria)) * '0') + binarioMemoria
        binarioMemoria = binarioMemoria[32 - (8 * (pulo+1)) : 32 - (8 * pulo)]
        armazenaRegistradores(registrador1, binarioMemoria)


def instrucaoSLL(binario, numero):
    binario = binario + (numero * '0') # preenche o binario com zeros a direita
    binario = binario[(len(binario)) - 32:] if len(binario) > 32 else binario # pega os 32 primeiros bits do binario
    return binario

def instrucaoSRL(binario, numero):
    binario = ('0' * numero) + binario # preenche o binario com zeros a esquerda
    binario = binario[:-numero] if numero != 0 else binario
    return binario

def instrucaoSRA(binario, numero): # preenche o binario com zeros a esquerda
    if len(binario) < 32 or binario[0] == '0': 
        binario = instrucaoSRL(binario, numero)
        return binario
    else:
        binario = ('1' * numero) + binario # preenche o binario com uns a esquerda
        binario = binario[:-numero] if numero != 0 else binario
        return binario


def instrucaoAnd(binario1, binario2):
    listaAndBinario = [] # cria uma lista para armazenar a operacao binaria de and
    for i in range( len(binario1) ):
        listaAndBinario.append( str(int(binario1[i]) and int(binario2[i])) ) # lista vai armazenandoo and bit a bit
    andBinario = ''.join(listaAndBinario) # variavel que armazena uma string da lista anterior

    # armazena o andBinario
    return andBinario

def instrucaoOr(binario1, binario2):
    listaOrBinario = [] # cria uma lista para armazenar a operacao binaria de or
    for i in range(len(binario1)):
        listaOrBinario.append(str( int(binario1[i]) or int(binario2[i])) ) # realiza a operacao de or bit a bit e armazena na lista
    orBinario = ''.join(listaOrBinario) # variavel que armazena uma string do conteudo da lista

    # devolve orBinario
    return orBinario

def instrucaoXor(binario1, binario2):
    listaXorBinario = [] # cria uma lista para armazenar a operacao binaria de xor
    for i in range(len(binario1)):
        listaXorBinario.append( '0' if binario1[i] == binario2[i] else '1' )  # realiza a operacao de xor bit a bit e armazena na lista
    xorBinario = ''.join(listaXorBinario)  # variavel que armazena uma string do conteudo da lista

    # devolve xorBinario
    return xorBinario

def instrucaoNor(binario1, binario2):
    listaNorBinario = [] # cria uma lista para armazenar a operacao binaria de xor
    binario1, binario2 = ('0' * (32 - len(binario1)) + binario1), ('0' * (32 - len(binario2)) + binario2) # completa os dois binarios com 0 a esquerda
    orBinario = instrucaoOr(binario1, binario2) # armazena o or entre os dois binarios

    for i in orBinario: # percorre o orBinario
        listaNorBinario.append('0' if i == '1' else '1') # inverte cada bit do orBinario (transformando ele num nor)
    norBinario = ''.join(listaNorBinario) # armazena a lista em norBinario no formato de string

    #devolve norBinario
    return norBinario


# imprime os registradores na ordem
def devolveRegistradores():
    listaRegistradores = []

    for i in range(31):
        listaRegistradores.append("$" + str(i) + " = " + registradores["$" + str(i)] + '; ')
    listaRegistradores.append("$31 = " + registradores["$31"] + ";")

    return ''.join(listaRegistradores)


main()
