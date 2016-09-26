listaEntrada =[]
listaSaidabin = []
listaSaida = []
with open("entrada.txt") as entrada, open("saidabin.txt") as saidabin, open("saida.txt") as saida:
    for linha in entrada.readlines():
        listaEntrada.append(linha)
        
    for linha in saidabin.readlines():
        listaSaidabin.append(linha)
        
    for linha in saida.readlines():
        listaSaida.append(linha)
    
with open("caminho.txt", 'w') as caminho:
    for i in range(40):
        print(listaEntrada[i] + listaSaidabin[i] + listaSaida[i], file = caminho)
    
