def ler_entrada():
    lista_numeros = input().split()
    lista_inteiros = []
    for numero in lista_numeros:
        lista_inteiros.append(int(numero))
    return lista_inteiros


def maior(lista, primeiro, ultimo):
    if primeiro == ultimo:
        return lista[primeiro]
    else:
        numero_meio = (primeiro + ultimo) // 2
        maior_inicio = maior(lista, primeiro, numero_meio)
        maior_fim = maior(lista, numero_meio + 1, ultimo)
        if maior_inicio >= maior_fim:
            return maior_inicio
        else:
            return maior_fim


def main():
    lista_numeros = ler_entrada()
    maior_numero = maior(lista_numeros, 0, len(lista_numeros) - 1)
    print(maior_numero)


main()