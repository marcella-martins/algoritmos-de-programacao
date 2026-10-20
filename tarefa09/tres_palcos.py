def ler_entrada():
    shows_programados = int(input())
    lista_artistas = []
    tempo = []
    for show in range(shows_programados):
        artista, duracao = input().split()
        lista_artistas.append(artista)
        tempo.append(int(duracao))
    return lista_artistas, tempo


def atribuir_shows(nomes, tempos):
    tamanho = len(nomes)
    melhor_divisao = None
    soma_shows = [0] * (tamanho + 1)
    for a in range(tamanho):
        soma_shows[a + 1] = soma_shows[a] + tempos[a]
    for i in range(1, tamanho - 1):
        for j in range(i + 1, tamanho):
            soma_palco1 = soma_shows[i] - soma_shows[0]
            soma_palco2 = soma_shows[j] - soma_shows[i]
            soma_palco3 = soma_shows[tamanho] - soma_shows[j]
            duracao = max(soma_palco1, soma_palco2, soma_palco3)
            if melhor_divisao is None:
                melhor_divisao = (duracao, i, j)
            else:
                melhor_duracao, melhor_i, melhor_j = melhor_divisao
                if duracao < melhor_duracao:
                    melhor_divisao = (duracao, i, j)
                elif duracao == melhor_duracao:
                    if i > melhor_i:
                        melhor_divisao = (duracao, i, j)
                    elif i == melhor_i and (j - i) > (melhor_j - melhor_i):
                        melhor_divisao = (duracao, i, j)
    duracao, i, j = melhor_divisao
    artistas1 = nomes[:i]
    artistas2 = nomes[i:j]
    artistas3 = nomes[j:]
    tempo1 = soma_shows[i] - soma_shows[0]
    tempo2 = soma_shows[j] - soma_shows[i]
    tempo3 = soma_shows[tamanho] - soma_shows[j]
    artistas = [artistas1, artistas2, artistas3]
    duracoes = [tempo1, tempo2, tempo3]
    return artistas, duracoes


def main():
    artistas, tempos = ler_entrada()
    palcos_divididos, duracao_palco = atribuir_shows(artistas, tempos)
    for palco in range(3):
        shows_palco = ", ".join(palcos_divididos[palco])
        print(f"Palco {palco + 1}: {shows_palco} ({duracao_palco[palco]} minutos)")
    print(f"Duração do festival: {max(duracao_palco)} minutos")


main()
