BRANCO = 255
PRETO = 0
def ler_arquivos():
    entrada = input()
    saida = input()
    return entrada, saida

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
    return int(n), int(m), intensidade, matriz, escala

def encontrar_limites(n, m, matriz):
    minimo = matriz[0][0]
    maximo = matriz[0][0]
    for i in range(m):
        for j in range(n):
            if matriz[i][j] < minimo:
                minimo = matriz[i][j]
            if matriz[i][j] > maximo:
                maximo = matriz[i][j]
    return minimo, maximo

def normalizar_imagem(n, m, minimo, maximo, matriz):
    matriz_normalizada = []
    for i in range(m):
        linha_normalizada = []
        for j in range(n):
            linha_normalizada.append(int((matriz[i][j] - minimo) * 255 / (maximo - minimo)))
        matriz_normalizada.append(linha_normalizada)
    return matriz_normalizada

def contagem(m, n, matriz):
    numero_maximo = 0
    numero_minimo = 0
    for i in range(m):
        for j in range(n):
            if matriz[i][j] == PRETO:
                numero_minimo += 1
            if matriz[i][j] == BRANCO:
                numero_maximo += 1
    return numero_minimo, numero_maximo

def criar_saida(saida, n, m, matriz_normalizada, escala, intensidade):
    with open(saida, "w") as foto:
        foto.write(f"{escala}\n")
        foto.write(f"# {saida}\n")
        foto.write(f"{n} {m}\n")
        foto.write(f"{intensidade}\n")
        for i in range(m):
            for j in range(n):
                foto.write(f"{matriz_normalizada[i][j]} ")
            foto.write("\n")

def imprimir(saida, numero_minimo, numero_maximo, entrada, n, m, matriz):
    minimo_inicial, maximo_inicial = contagem(m, n, matriz)
    print(f"{entrada}: {minimo_inicial} pixels pretos e {maximo_inicial} pixels brancos")
    print(f"{saida}: {numero_minimo} pixels pretos e {numero_maximo} pixels brancos")

def main():
    entrada, saida = ler_arquivos()
    n, m, intensidade, matriz, escala = imagem_inicial(entrada)
    minimo, maximo = encontrar_limites(n, m, matriz)
    matriz_normalizada = normalizar_imagem(n, m, minimo, maximo, matriz)
    numero_minimo, numero_maximo = contagem(m, n, matriz_normalizada)
    criar_saida(saida, n, m, matriz_normalizada, escala, intensidade)
    imprimir(saida, numero_minimo, numero_maximo, entrada, n, m, matriz)

if __name__ == "__main__":
    main()