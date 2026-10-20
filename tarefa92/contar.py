def ler_entrada():
    entrada = input()
    return entrada


def imagem_inicial(entrada):
    with open(entrada) as arquivo:
        dados = arquivo.read().split("\n")
    escala = dados[0]
    n, m = dados[2].split()
    intensidade = dados[3]
    numeros = " ".join(dados[4:]).split()
    matriz = []
    pos = 0
    for i in range(int(m)):
        linha_matriz = []
        for j in range(int(n)):
            linha_matriz.append(int(numeros[pos]))
            pos += 1
        matriz.append(linha_matriz)
    return int(n), int(m), matriz


def pintar_colonias(n, m, matriz):
    """
    O problema entra com as coordenadas de um pixel, o qual pertence a uma
    colônia dentro da matriz imagem, e a própria matriz imagem.
    Como saída, uma matriz atualizada, com todos os pixels tendo valor de
    255, o que indica que já foram visitados e contados.
    A partir da posição atual, um caso básico é quando nenhum dos pixels
    adjacentes têm valor 0, ou está na borda da matriz, não havendo vizinhos
    na direção designada. Assim, a função não faz mais chamadas recursivas.
    Há redução a menores instâncias quando, a cada chamada, a função verifica
    os pixels adjacentes ao atual. E, ao encontrar um com valor 0, ela marca
    esse com 255 e se chama, passando as coordenadas do novo pixel.
    """
    if m != 0:
        if matriz[m - 1][n] == 0:
            matriz[m - 1][n] = 255
            matriz = pintar_colonias(n, m - 1, matriz)
    if n != 0:
        if matriz[m][n - 1] == 0:
            matriz[m][n - 1] = 255  
            matriz = pintar_colonias(n - 1, m, matriz)  
    if m != len(matriz) - 1:
        if matriz[m + 1][n] == 0:
            matriz[m + 1][n] = 255
            matriz = pintar_colonias(n, m + 1, matriz)
    if n != len(matriz[m]) - 1:
        if matriz[m][n + 1] == 0:
            matriz[m][n + 1] = 255
            matriz = pintar_colonias(n + 1, m, matriz)
    return matriz


def contar_colonias(n, m, matriz):
    numero_colonias = 0
    for i in range(m):
        for j in range(n):
            if matriz[i][j] == 0:
                numero_colonias += 1
                matriz[i][j] = 255
                matriz = pintar_colonias(j, i, matriz)
    return numero_colonias


def main():
    entrada = ler_entrada()
    coluna, linha, matriz = imagem_inicial(entrada)
    numero_colonias = contar_colonias(coluna, linha, matriz)
    print(f"A imagem tem {numero_colonias} colônias.")


main()
