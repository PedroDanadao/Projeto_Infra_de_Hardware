def converteParaBinario(hexa):
    base = 16 ## equals to hexadecimal
    bits = 8

    binario = bin(int(hexa, base))[2:].zfill(bits)
    binario = str(binario)
    
    for i in range(32 - len(binario)):
        binario = '0' + binario
        
    return binario
   

with open("entrada.txt") as entrada, open ("saidabin.txt", 'w') as saidabin:
    for linha in entrada.readlines():
        binario = converteParaBinario(linha)
        print(binario, file = saidabin)
        
