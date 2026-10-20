import math
from normalizar import imagem_inicial, encontrar_limites, normalizar_imagem
from binarizar import ler_infos, filtro_maioria
PRETO = 0
LIMITE_INFERIOR = 30
LIMITE_SUPERIOR = 300
def ler_entrada():
    entrada = input()
    largura, limiar, fator = ler_infos()
    abscissa, ordenada, raio = input().split()
    n_medio = input()
    return entrada, largura, limiar, fator, int(abscissa), int(ordenada), int(raio), int(n_medio)


def contar_pixels(n, m, matriz, abscissa, ordenada, raio):
    total = 0
    for i in range(m):
        for j in range(n):
            pixel_x = j
            pixel_y = m - 1 - i
            distancia = math.sqrt((pixel_x - abscissa) ** 2 + (pixel_y - ordenada) ** 2)
            if distancia <= raio and matriz[i][j] == PRETO:
                total += 1
    return total


def classificar_placa(numero_colonias):
    if numero_colonias < LIMITE_INFERIOR:
        return "Placa inadequada, dilua menos a amostra."
    elif numero_colonias > LIMITE_SUPERIOR:
        return "Placa inadequada, dilua mais a amostra."
    else:
        return "Placa adequada para contagem."


def main():
    entrada, largura, limiar, fator, abscissa, ordenada, raio, n_medio = ler_entrada()
    n, m, intensidade, matriz, escala = imagem_inicial(entrada)
    minimo, maximo = encontrar_limites(n, m, matriz)
    matriz_normalizada = normalizar_imagem(n, m, minimo, maximo, matriz)
    matriz_binarizada = filtro_maioria(n, m, matriz_normalizada, largura, limiar, fator)
    pixels_colonias = contar_pixels_no_disco(n, m, matriz_binarizada, abscissa, ordenada, raio)
    numero_colonias = pixels_colonias // n_medio
    print(f"Número de colônias estimado: {numero_colonias}")
    print(classificar_placa(numero_colonias))


main()
