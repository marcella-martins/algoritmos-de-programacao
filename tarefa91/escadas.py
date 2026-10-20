def escada():
    numero = input()
    tamanho = len(numero)
    numeros_escadas = True
    while True:
        for i in range(tamanho):
            if not i == 0:
                if int(numero[i-1]) == int(numero[i]) + 1 or int(numero[i-1]) == int(numero[i]) - 1:
                    pass
                else:
                    numeros_escadas = False
            if not i == int(tamanho - 1):
                if int(numero[i+1]) == int(numero[i]) + 1 or int(numero[i+1]) == int(numero[i]) - 1:
                    pass
                else:
                    numeros_escadas = False
        break
    return numero, numeros_escadas

def main():
    entradas = input()
    for i in range(0, int(entradas)):
        numero, numeros_escadas = escada()
        if numeros_escadas == True:
            print(f"{numero} é um escada")
        else:
            print(f"{numero} não é um escada")
            
main()