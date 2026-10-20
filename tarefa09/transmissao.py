def ler_entrada():
    total_generos = int(input())
    generos = input().split()
    total_shows = int(input())
    shows = []
    for show in range(total_shows):
        artista, genero = input().split()
        shows.append((artista, genero))
    return generos, shows


def encontrar_trecho(generos, shows):
    total_shows = len(shows)
    generos = set(generos)
    total_generos = len(generos)
    repeticao_genero = {}
    generos_diferentes = 0
    inicio = None
    fim = None
    esquerda = 0
    for direita in range(total_shows):
        genero_direita = shows[direita][1]
        if genero_direita in generos:
            repeticao_genero[genero_direita] = repeticao_genero.get(genero_direita, 0) + 1
            if repeticao_genero[genero_direita] == 1:
                generos_diferentes += 1
        while generos_diferentes == total_generos:
            tamanho = direita - esquerda + 1
            if inicio is None or tamanho < (fim - inicio + 1):
                inicio = esquerda
                fim = direita
            genero_esquerda = shows[esquerda][1]
            if genero_esquerda in generos:
                repeticao_genero[genero_esquerda] -= 1
                if repeticao_genero[genero_esquerda] == 0:
                    generos_diferentes -= 1
            esquerda += 1
    if inicio is None:
        return []
    else:
        return shows[inicio:fim + 1]


def main():
    generos, shows = ler_entrada()
    trecho_shows = encontrar_trecho(generos, shows)
    if len(generos) == 1:
        print(f"Menor trecho tem {len(trecho_shows)} show:")
    else:
        print(f"Menor trecho tem {len(trecho_shows)} shows:")
    for artista, genero in trecho_shows:
        print(f"- {artista} ({genero})")


main()