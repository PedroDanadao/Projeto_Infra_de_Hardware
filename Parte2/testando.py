
HEXA = "0x3c010002"

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
registradores = {"$0":"0",  "$1":"0",  "$2":"13",  "$3":"-31",  "$4":"0",
"$5":"0",  "$6":"0",  "$7":"0",  "$8":"0",  "$9":"0",  "$10":"0",
"$11":"0",  "$12":"0",  "$13":"0",  "$14":"0",  "$15":"0",  "$16":"0",
"$17":"0",  "$18":"0",  "$19":"0",  "$20":"0",  "$21":"0",  "$22":"0",
"$23":"0",  "$24":"0",  "$25":"0",  "$26":"0",  "$27":"0",  "$28":"0",
"$29":"0",  "$30":"0",  "$31":"0"}

def main():
    binario = converteParaBinario(HEXA) # converte o hexadecimal recebido para binario
    tipo = defineTipo(binario) # pega o tipo de codigo do hexadecimal(r, i, j, s)
    escreveCodigo(binario, tipo) # escreve o codigo na tela'''
    #imprimeRegistradores()
    '''with open("entrada.txt") as entrada, open("saida.txt", 'w') as saida:
        for linha in entrada.readlines():
            binario = converteParaBinario(linha) # converte o hexadecimal da linha para binario
            tipo = defineTipo(binario) # pega o tipo de codigo do hexadecimal(r, i, j, s)
            print(escreveCodigo(binario, tipo), file = saida) # escreve o codigo no arquivo de saida'''
            

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

def escreveCodigo(binario, tipo):
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
            # vvvvvvvvvvvvvvvvvvvvvvvvvvv
            operacaoAritmetica(func, '$' + registrador1, '$' + registrador2, numero = numero)
        elif func in ("sllv", "srlv", "srav"): # caso o func seja um desses
            registrador1, registrador2, registrador3 = str(int(binario[16:21], 2)), str(int(binario[11:16], 2)), str(int(binario[6:11], 2))
            codigo = func + ' $' + registrador1 + ', $' + registrador2 + ', $' + registrador3
            # vvvvvvvvvvvvvvvvvvvvvvvvvvv
            operacaoAritmetica(func, '$' + registrador1, '$' + registrador2, '$' + registrador3)
        else: # caso o func nao seja nenhum dos acima (ou seja, func eh dos que usam tres registradores, como 'add' ou 'sub')
            registrador1, registrador2, registrador3 = str(int(binario[16:21], 2)), str(int(binario[6:11], 2)), str(int(binario[11:16], 2))
            codigo = func + ' $' + registrador1 + ', $' + registrador2 + ', $' + registrador3
            # vvvvvvvvvvvvvvvvvvvvvvvvvvv
            operacaoAritmetica(func, '$' + registrador1, '$' + registrador2, '$' + registrador3)
            operacaoLogica(func, '$' + registrador1, '$' + registrador2, '$' + registrador3)

    elif tipo == 'ij': # caso o comando seja do tipo 'i' ou 'j'
        func = tipoIJ[ binario[:6] ]

        if func == "lui": # caso o func seja 'lui'
            registrador, numero = str(int(binario[11:16], 2)), int(binario[16:32], 2) # registrador eh igual a sequencia binaria do 11 bit ao 16 bit. numero vai ser o resto da sequencia binaria
            codigo = func + ' $' + registrador + ', ' + str(numero)
            # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            operacaoAritmetica(func, '$' + registrador, numero = numero)
        elif func == "bltz": # caso o func seja 'bltz'
            registrador = str(int(binario[6:11], 2))
            codigo = func + ' $' + registrador + ', start'
        elif func in ("addi", "slti", "andi", "ori", "xori", "addiu"): # se func for um desses
            registrador1, registrador2, numero = str(int(binario[11:16], 2)), str(int(binario[6:11], 2)), int(binario[17:32], 2) # dessa vez ele conta do 17 bit ao fim, pois o 16 vai servir pra checar se o numero eh negativo
            numero = numero - 32768 if binario[16] == '1' else numero # caso o numero seja negativo, ele vai ser: numero - 32768. mais em https://www.youtube.com/watch?v=ZwRfnmXY7VY
            codigo = func + ' $' + registrador1 + ', $' + registrador2 + ', ' + str(numero)
            operacaoAritmetica(func, '$' + registrador1, '$' + registrador2, numero = numero)
            operacaoLogica(func, '$' + registrador1, '$' + registrador2, numero = numero)
            
        elif func in ("lw", "sw", "lb", "lbu", "sb"):
            registrador1, registrador2, numero = str(int(binario[11:16], 2)), str(int(binario[6:11], 2)), int(binario[17:32], 2) # dessa vez ele conta do 17 bit ao fim, pois o 16 vai servir pra checar se o numero eh negativo
            numero = numero - 32768 if binario[16] == '1' else numero # caso o numero seja negativo, ele vai ser: numero - 32768. mais em https://www.youtube.com/watch?v=ZwRfnmXY7VY
            codigo = func + ' $' + registrador1 + ', ' + str(numero) + '($' + registrador2 + ')'
        elif func in ("beq", "bne"):
            registrador1, registrador2 = str(int(binario[6:11], 2)), str(int(binario[11:16], 2))
            codigo = func + ' $' + registrador1 + ', $' + registrador2 + ', start'
        elif func in ("j", "jal"):
            codigo = func + ' start'

    return codigo

###########################################################################################################################################
#funcao que vai realizar a operacao aritmetica especificada pelo codigo e armazenar o resultado nos registradores especificos
def operacaoAritmetica(func, registrador1, registrador2 = '', registrador3 = '', numero = None):
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
        binNumero = decimalParaBinario(numero) + ( '0' * 16 )
        registradores[registrador1] =binarioParaDecimal(binNumero)
        imprimeRegistradores()

    if func == "sll":
        binReg2 = decimalParaBinario( int(registradores[registrador2]) )
        binReg2 = binReg2 + (numero * '0')
        binReg2 = binReg2[(len(binReg2)) - 32:] if len(binReg2) > 32 else binReg2
        registradores[registrador1] = binarioParaDecimal(binReg2)

    if func == "srl":
        binReg2 = decimalParaBinario(int(registradores[registrador2]))
        binReg2 = ('0' * numero) + binReg2
        binReg2 = binReg2[:-numero] if numero != 0 else binReg2
        registradores[registrador1] = binarioParaDecimal(binReg2)

    if func == "sra":
        binReg2 = decimalParaBinario(int(registradores[registrador2]))
        if int( registradores[registrador2] ) >= 0:
            binReg2 = ('0' * numero) + binReg2
            binReg2 = binReg2[:-numero] if numero != 0 else binReg2
            registradores[registrador1] = binarioParaDecimal(binReg2)
        else:
            binReg2 = ('1' * numero) + binReg2
            binReg2 = binReg2[:-numero] if numero != 0 else binReg2
            registradores[registrador1] = binarioParaDecimal(binReg2)

    if func == "sllv":
        pulo = int( registradores[registrador3] )
        binReg2 = decimalParaBinario(int(registradores[registrador2]))
        if pulo >= 0:
            binReg2 = binReg2 + ( (pulo % 32) * '0' )
            binReg2 = binReg2[(len(binReg2)) - 32:] if len(binReg2) > 32 else binReg2
            registradores[registrador1] = binarioParaDecimal(binReg2)
        else:
            binReg2 = binReg2[pulo:] + ((32 + pulo) * '0')
            binReg2 = binReg2[(len(binReg2)) - 32:] if len(binReg2) > 32 else binReg2
            registradores[registrador1] = binarioParaDecimal(binReg2)

    if func == "srlv":
        pulo = int( registradores[registrador3] )
        binReg2 = decimalParaBinario(int(registradores[registrador2]))
        if (pulo % 32) >= 0:
            binReg2 = ('0' * (pulo % 32)) + binReg2
            binReg2 = binReg2[: -(pulo % 32) ] if (pulo % 32) != 0 else binReg2
            registradores[registrador1] = binarioParaDecimal(binReg2)
        else:
            binReg2 = ( '0' * (32 - (pulo % 32)) ) + binReg2
            binReg2 = binReg2[:-(pulo % 32)] if (pulo % 32) != 0 else binReg2
            registradores[registrador1] = binarioParaDecimal(binReg2)

    if func == "srav":
        pulo = int( registradores[registrador3] )
        binReg2 = decimalParaBinario(int(registradores[registrador2]))
        if (pulo % 32) >= 0:
            if int(registradores[registrador2]) >= 0:
                binReg2 = ('0' * (pulo % 32)) + binReg2
                binReg2 = binReg2[:-(pulo % 32)] if (pulo % 32) != 0 else binReg2
                registradores[registrador1] = binarioParaDecimal(binReg2)
            else:
                binReg2 = ('1' * (pulo % 32)) + binReg2
                binReg2 = binReg2[:-(pulo % 32)] if (32 % pulo) != 0 else binReg2
                registradores[registrador1] = binarioParaDecimal(binReg2)
        else:
            if int(registradores[registrador2]) >= 0:
                binReg2 = ('0' * ( 32 - (pulo % 32)) ) + binReg2
                binReg2 = binReg2[ :(32 - (32 % pulo)) ] if (32 - (32 % pulo)) != 0 else binReg2
                registradores[registrador1] = binarioParaDecimal(binReg2)
            else:
                binReg2 = ('1' * (32 - (32 % pulo))) + binReg2
                binReg2 = binReg2[ :- (32 - (32 % pulo)) ] if (32 - (32 % pulo)) != 0 else binReg2
                registradores[registrador1] = binarioParaDecimal(binReg2)


# funcao que recebe o primeiro registrador e os demais dados(se necessario), e realiza as operacoes logicas acesseando e armazenando
# em registradores
def operacaoLogica(func, registrador1, registrador2 = '', registrador3 = '', numero = None):
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
        listaAndBinario = [] # cria uma lista para armazenar a operacao binaria de and
        for i in range(maior):
            listaAndBinario.append( str(int(binReg2[i]) and int(binReg3[i])) ) # lista vai armazenandoo and bit a bit
        andBinario = ''.join(listaAndBinario) # variavel que armazena uma string da lista anterior

        # armazena o andBinario em decimal (lida com binarios negativos tambem)
        registradores[registrador1] = str( int(andBinario, 2) ) if len(andBinario) != 32 or andBinario[0] == '0' else str( int(andBinario[1:], 2) -  2147483648)
        #imprimeRegistradores()

    if func == "or": # or bit a bit
        listaOrBinario = [] # cria uma lista para armazenar a operacao binaria de or
        for i in range(maior):
            listaOrBinario.append(str( int(binReg2[i]) or int(binReg3[i])) ) # realiza a operacao de or bit a bit e armazena na lista
        orBinario = ''.join(listaOrBinario) # variavel que armazena uma string do conteudo da lista

        # armazena orBinario, em decimal, no registrador1 (tambem lida com binarios negativos)
        registradores[registrador1] = str(int(orBinario, 2)) if len(orBinario) != 32 or orBinario[0] == '0' else str( int(orBinario[1:], 2) - 2147483648 )
        #imprimeRegistradores()

    if func == "xor": # xor bit a bit (bit != bit => 1  /  bit == bit => 0)
        listaXorBinario = [] # cria uma lista para armazenar a operacao binaria de xor
        for i in range(maior):
            listaXorBinario.append( '0' if binReg2[i] == binReg3[i] else '1' )  # realiza a operacao de xor bit a bit e armazena na lista
        xorBinario = ''.join(listaXorBinario)  # variavel que armazena uma string do conteudo da lista

        # armazena xorBinario, em decimal, no registrador1 (tambem lida com binarios negativos)
        registradores[registrador1] = str(int(xorBinario, 2)) if len(xorBinario) != 32 or xorBinario[0] == '0' else str( int(xorBinario[1:], 2) - 2147483648 )
        #imprimeRegistradores()

    if func == "nor": # nor bit a bit (not or)
        listaNorBinario = [] # cria uma lista para armazenar a operacao binaria de nor
        binReg2, binReg3 = ('0' * (32 - len(binReg2))) + binReg2, ( '0' * (32 - len(binReg3)) ) # nesse caso temos que analizar todos os 32 bits

        for i in range(32):
            listaNorBinario.append( '0' if int( binReg2[i] ) or int( binReg3[i] ) else '1' )  # realiza a operacao de nor bit a bit e armazena na lista
        norBinario = ''.join(listaNorBinario)  # variavel que armazena uma string do conteudo da lista
        print(norBinario)

        # armazena norBinario, em decimal, no registrador1 (tambem lida com binarios negativos)
        registradores[registrador1] = str(int(norBinario, 2)) if len(norBinario) != 32 or norBinario[0] == '0' else str( int(norBinario[1:], 2) - 2147483648 )
        imprimeRegistradores()

    if func == "andi":
        listaAndIBinario = []  # cria uma lista para armazenar a operacao binaria de andi
        for i in range(maior):
            listaAndIBinario.append( str(int(binReg2[i]) and int(binNum[i])) )  # lista vai armazenandoo and bit a bit
        andiBinario = ''.join(listaAndIBinario)  # variavel que armazena uma string da lista anterior

        # armazena o andiBinario em decimal (lida com binarios negativos tambem)
        registradores[registrador1] = str(int(andiBinario, 2)) if len(andiBinario) != 32 or andiBinario[0] == '0' else str( int(andiBinario[1:], 2) - 2147483648 )
        imprimeRegistradores()

    if func == "ori":
        listaOrIBinario = []  # cria uma lista para armazenar a operacao binaria de ori
        for i in range(maior):
            listaOrIBinario.append( str(int(binReg2[i]) or int(binNum[i])) )  # realiza a operacao de or bit a bit e armazena na lista
        oriBinario = ''.join(listaOrIBinario)  # variavel que armazena uma string da lista anterior
        print(oriBinario)

        # armazena o oriBinario em decimal (lida com binarios negativos tambem)
        registradores[registrador1] = str(int(oriBinario, 2)) if len(oriBinario) != 32 or oriBinario[0] == '0' else str( int(oriBinario[1:], 2) - 2147483648 )
        imprimeRegistradores()

    if func == "xori":
        listaXorIBinario = []  # cria uma lista para armazenar a operacao binaria de andi
        for i in range(maior):
            listaXorIBinario.append( '0' if binReg2[i] == binNum[i] else '1' )  # realiza a operacao de xor bit a bit e armazena na lista
        xoriBinario = ''.join(listaXorIBinario)  # variavel que armazena uma string da lista anterior

        # armazena o xoriBinario em decimal (lida com binarios negativos tambem)
        registradores[registrador1] = str( int(xoriBinario, 2) ) if len(xoriBinario) != 32 or xoriBinario[0] == '0' else str( int(xoriBinario[1:], 2) - 2147483648 )
        imprimeRegistradores()


# imprime os registradores na ordem
def imprimeRegistradores():
    for i in range(31):
        print("$" + str(i) + " = " + registradores["$" + str(i)], end = ", ")
    print("$31 = " + registradores["$31"] + ";")


main()
