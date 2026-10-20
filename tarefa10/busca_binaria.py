def ler_entrada():
    lista_numeros = input().split()
    repeticao = input()
    lista_inteiros = []
    for numero in lista_numeros:
        lista_inteiros.append(int(numero))
    return lista_inteiros, int(repeticao)


def buscar(lista, x, inicio, fim, tipo_busca):
    metade = (inicio + fim) // 2
    if lista[metade] == x:
        if tipo_busca:
            if metade == inicio or lista[metade - 1] != x:
                return metade
            else:
                return buscar(lista, x, inicio, metade - 1, tipo_busca)
        else:
            if metade == fim or lista[metade + 1] != x:
                return metade
            else:
                return buscar(lista, x, metade + 1, fim, tipo_busca)
    elif lista[metade] > x:
        return buscar(lista, x, metade + 1, fim, tipo_busca)
    else:
        return buscar(lista, x, inicio, metade - 1, tipo_busca)


def main():
    lista, x = ler_entrada()
    if x not in lista:
        print(0)
    else:
        primeiro_caso = int(buscar(lista, x, 0, len(lista) - 1, True))
        ultimo_caso = int(buscar(lista, x, 0, len(lista) - 1, False))
        numero_repeticoes = (ultimo_caso - primeiro_caso + 1)
        print(numero_repeticoes)


main()
