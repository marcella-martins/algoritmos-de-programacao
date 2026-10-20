def ler_entrada():
    tamanho = int(input())
    matriz = []
    for i in range(tamanho):
        linha = [float(elemento) for elemento in input().split()]
        matriz.append(linha)
    return tamanho, matriz


def construir_matriz(matriz, linha_removida, coluna_removida):
    menor_matriz = []
    for i in range(len(matriz)):
        if i == linha_removida:
            continue
        nova_linha = []
        for j in range(len(matriz[i])):
            if j == coluna_removida:
                continue
            nova_linha.append(matriz[i][j])
        menor_matriz.append(nova_linha)
    return menor_matriz


def calcular_determinante(matriz):
    tamanho_matriz = len(matriz)
    if tamanho_matriz == 1:
        return matriz[0][0]
    det = 0
    for i in range(tamanho_matriz):
        menor_matriz = construir_matriz(matriz, 0, i)
        cofator = ((-1) ** i) * calcular_determinante(menor_matriz)
        det += matriz[0][i] * cofator
    return det


def main():
    n, matriz = ler_entrada()
    if n == 0:
        determinante = 1.0
    else:
        determinante = calcular_determinante(matriz)
    print(f"{determinante:.2f}")


main()