def ler_entrada():
    lista_numeros = input().split()
    lista_inteiros = []
    for numero in lista_numeros:
        lista_inteiros.append(int(numero))
    return lista_inteiros


def reorganizar_lista(lista, inicio, fim):
    pivo = lista[inicio]
    esquerda = inicio + 1
    direita = fim - 1
    while True:
        while esquerda <= direita and lista[esquerda] <= pivo:
            esquerda += 1
        while esquerda <= direita and lista[direita] > pivo:
            direita -= 1
        if esquerda > direita:
            break
        lista[esquerda], lista[direita] = lista[direita], lista[esquerda]
    lista[inicio], lista[direita] = lista[direita], lista[inicio]
    return direita


def quick_sort(lista, inicio=0, fim=None):
    if fim is None:
        fim = len(lista)
    if fim - inicio > 1:
        indice_pivo = reorganizar_lista(lista, inicio, fim)
        quick_sort(lista, inicio, indice_pivo)
        quick_sort(lista, indice_pivo + 1, fim)
    return lista


def main():
    lista = ler_entrada()
    quick_sort(lista)
    strings_numeros = []
    for x in lista:
        strings_numeros.append(str(x))
    lista_ordenada = ' '.join(strings_numeros)
    print(lista_ordenada)


main()