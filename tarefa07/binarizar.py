from normalizar import ler_arquivos, imagem_inicial, encontrar_limites, normalizar_imagem, contagem, criar_saida

def ler_infos():
    largura, limiar, fator = input().split()
    return int(largura), int(limiar), float(fator)

def filtro_maioria(n, m, matriz, largura, limiar, fator):
    metade = largura // 2
    total_janela = largura * largura
    matriz_binarizada = []
    for i in range(m):
        linha_binarizada = []
        for j in range(n):
            pixel = 0
            for x in range(i - metade, i + metade + 1):
                for y in range(j - metade, j + metade + 1):
                    if 0 <= x < m and 0 <= y < n:
                        if matriz[x][y] <= limiar:
                            pixel += 1
            if pixel >= fator * total_janela:
                linha_binarizada.append(0)
            else:
                linha_binarizada.append(255)
        matriz_binarizada.append(linha_binarizada)
    return matriz_binarizada

def main():
    entrada, saida = ler_arquivos()
    largura, limiar, fator = ler_infos()
    n, m, intensidade, matriz, escala = imagem_inicial(entrada)
    minimo, maximo = encontrar_limites(n, m, matriz)
    matriz_normalizada = normalizar_imagem(n, m, minimo, maximo, matriz)
    matriz_binarizada = filtro_maioria(n, m, matriz_normalizada, largura, limiar, fator)
    criar_saida(saida, n, m, matriz_binarizada, escala, intensidade)
    minimo_original, maximo_original = contagem(m, n, matriz)
    minimo_binarizado, maximo_binarizado = contagem(m, n, matriz_binarizada)
    print(f"{entrada}: {minimo_original} pixels pretos e {maximo_original} pixels brancos")
    print(f"{saida}: {minimo_binarizado} pixels pretos e {maximo_binarizado} pixels brancos")
    
if __name__ == "__main__":
    main()