HEXA = "0x00200008"

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


def main():
    with open("entrada.txt") as entrada, open("saida2.txt", 'w') as saida:
        for linha in entrada.readlines():
            binario = converteParaBinario(linha) # converte o hexadecimal da linha para binario
            tipo = defineTipo(binario) # pega o tipo de codigo do hexadecimal(r, i, j, s)
            print(escreveCodigo(binario, tipo), file = saida) # escreve o codigo no arquivo de saida
    '''binario = converteParaBinario(HEXA) # converte o hexadecimal recebido para binario
    tipo = defineTipo(binario) # pega o tipo de codigo do hexadecimal(r, i, j, s)
    print(escreveCodigo(binario, tipo)) # escreve o codigo na tela'''


def converteParaBinario(hexa):
    base = 16
    bits = 8

    binario = bin(int(hexa, base))[2:].zfill(bits)
    binario = str(binario)

    for i in range(32 - len(binario)):
        binario = '0' + binario

    return binario

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
            registrador = int(binario[6:11], 2) # registrador vai ser igual a sequencia binaria, do sexto bit ao decimo, na base 10
            codigo = func + ' $' + str(registrador) # codigo = 'jr' + $registrador
        elif func in ("mfhi", "mflo"): # caso o func seja "mfhi" ou "mflo"
            registrador = int(binario[16:21], 2)
            codigo = func + ' $' + str(registrador)
        elif func in ("mult", "multu", "div", "divu"): # caso o func seja um desses
            registrador1, registrador2 = int(binario[6:11], 2), int(binario[11:16], 2)
            codigo = func + ' $' + str(registrador1) + ', $' + str(registrador2)
        elif func in ("sll", "srl", "sra"): # caso o func seja um desses
            registrador1, registrador2, numero = int(binario[16:21], 2), int(binario[11:16], 2), int(binario[21:26], 2)
            codigo = func + ' $' + str(registrador1) + ', $' + str(registrador2) + ', ' + str(numero)
        elif func in ("sllv", "srlv", "srav"): # caso o func seja um desses
            registrador1, registrador2, registrador3 = int(binario[16:21], 2), int(binario[11:16], 2), int(binario[6:11], 2)
            codigo = func + ' $' + str(registrador1) + ', $' + str(registrador2) + ', $' + str(registrador3)
        else: # caso o func nao seja nenhum dos acima (ou seja, func eh dos que usam tres registradores, como 'add' ou 'sub')
            registrador1, registrador2, registrador3 = int(binario[16:21], 2), int(binario[6:11], 2), int(binario[11:16], 2)
            codigo = func + ' $' + str(registrador1) + ', $' + str(registrador2) + ', $' + str(registrador3)


    elif tipo == 'ij': # caso o comando seja do tipo 'i' ou 'j'
        func = tipoIJ[ binario[:6] ]
        
        if func == "lui": # caso o func seja 'lui'
            registrador, numero = int(binario[11:16], 2), int(binario[16:32], 2) # registrador eh igual a sequencia binaria do 11 bit ao 16 bit. numero vai ser o resto da sequencia binaria
            codigo = func + ' $' + str(registrador) + ', ' + str(numero)
        elif func == "bltz": # caso o func seja 'bltz'
            registrador = int(binario[6:11], 2)
            codigo = func + ' $' + str(registrador) + ', start'
        elif func in ("addi", "slti", "andi", "ori", "xori", "addiu"): # se func for um desses
            registrador1, registrador2, numero = int(binario[11:16], 2), int(binario[6:11], 2), int(binario[17:32], 2) # dessa vez ele conta do 17 bit ao fim, pois o 16 vai servir pra checar se o numero eh negativo
            numero = numero - 32768 if binario[16] == '1' else numero # caso o numero seja negativo, ele vai ser: numero - 32768. mais em https://www.youtube.com/watch?v=ZwRfnmXY7VY
            codigo = func + ' $' + str(registrador1) + ', $' + str(registrador2) + ', ' + str(numero)
        elif func in ("lw", "sw", "lb", "lbu", "sb"):
            registrador1, registrador2, numero = int(binario[11:16], 2), int(binario[6:11], 2), int(binario[17:32], 2) # dessa vez ele conta do 17 bit ao fim, pois o 16 vai servir pra checar se o numero eh negativo
            numero = numero - 32768 if binario[16] == '1' else numero # caso o numero seja negativo, ele vai ser: numero - 32768. mais em https://www.youtube.com/watch?v=ZwRfnmXY7VY
            codigo = func + ' $' + str(registrador1) + ', ' + str(numero) + '($' + str(registrador2) + ')'
        elif func in ("beq", "bne"):
            registrador1, registrador2 = int(binario[6:11], 2), int(binario[11:16], 2)
            codigo = func + ' $' + str(registrador1) + ', $' + str(registrador2) + ', start'
        elif func in ("j", "jal"):
            codigo = func + ' start'

    return codigo


main()
