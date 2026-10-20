def une_linhas(blocos):
    paragrafos = blocos.split("\n\n")
    novo_paragrafo = []
    for c in range(len(paragrafos)):
        paragrafo_dividido = paragrafos[c].split("\n")
        for d in range(1, len(paragrafo_dividido)):
            if paragrafo_dividido[0][-1] != " ":
                paragrafo_dividido[0] += " " + paragrafo_dividido[d]
            else:
                paragrafo_dividido[0] += paragrafo_dividido[d]
        novo_paragrafo.append(paragrafo_dividido[0])
    return novo_paragrafo

def quebra_paragrafos(paragrafos, largura):
    paragrafos_quebrados = []
    for paragrafo in paragrafos:
        proximo_paragrafo = paragrafo
        while len(proximo_paragrafo) > 0:
            if proximo_paragrafo[0] == " ":
                proximo_paragrafo = proximo_paragrafo[1:]
                continue
            if len(proximo_paragrafo) <= largura:
                paragrafos_quebrados.append(proximo_paragrafo)
                proximo_paragrafo = []
                break
            for i in range(largura, -1, -1):
                if len(proximo_paragrafo) - 1 >= i:
                    if proximo_paragrafo[i] == " ":
                        if i == largura:
                            paragrafos_quebrados.append(proximo_paragrafo[0:i])
                            proximo_paragrafo = proximo_paragrafo[i:]
                        else:
                            paragrafos_quebrados.append(proximo_paragrafo[0:i+1])
                            proximo_paragrafo = proximo_paragrafo[i+1:]
                        break
            else:
                paragrafos_quebrados.append(proximo_paragrafo[0:largura])
                proximo_paragrafo = proximo_paragrafo[largura:]
        paragrafos_quebrados.append("")
    if paragrafos_quebrados and paragrafos_quebrados[-1] == "":
        paragrafos_quebrados.pop()
    return paragrafos_quebrados

def centraliza_paragrafos(largura, paragrafos_quebrados):
    paragrafos_atualizados = list(paragrafos_quebrados)
    for a in range(len(paragrafos_atualizados)):
        if paragrafos_atualizados[a] == "":
            continue
        for j in range(((largura - len(paragrafos_atualizados[a])) // 2)):
            paragrafos_atualizados[a] = " " + paragrafos_atualizados[a] + " "
        if (largura - len(paragrafos_atualizados[a])) % 2 != 0:
            if paragrafos_atualizados[a][-1] != " ":
                paragrafos_atualizados[a] += " "
            else:
                paragrafos_atualizados[a] = " " + paragrafos_atualizados[a]
    return paragrafos_atualizados

def divide_paginas(linhas_folha, linhas_centralizadas):
    paginas = []
    while len(linhas_centralizadas) > 2 * linhas_folha:
        paginas.append(linhas_centralizadas[0:2 * linhas_folha])
        linhas_centralizadas = linhas_centralizadas[2 * linhas_folha:]
    paginas.append(linhas_centralizadas)
    return paginas

def cria_colunas(paginas, caracteres_linha, largura, linhas_folha):
    numero_espacos = caracteres_linha - (2 * largura)
    colunas_centralizadas = []
    for q in range(len(paginas)):
        segunda_coluna = []
        if len(paginas[q]) > linhas_folha:
            for x in range(linhas_folha, len(paginas[q])):
                segunda_coluna.append(paginas[q][x])
        for y in range(0, linhas_folha):
            if y < len(paginas[q]):
                coluna_um = str(paginas[q][y])
                if coluna_um == "":
                    coluna_um = " " * largura
            else:
                coluna_um = " " * largura
            if y < len(segunda_coluna):
                coluna_dois = str(segunda_coluna[y])
                if coluna_dois == "":
                    coluna_dois = " " * largura
            else:
                coluna_dois = " " * largura
            linha_nova = coluna_um + (numero_espacos * " ") + coluna_dois
            colunas_centralizadas.append(linha_nova)
    return colunas_centralizadas

def imprime_paginas(linhas_folha, colunas_centralizadas):
    i = 0
    for h in range(len(colunas_centralizadas)):
        if i < linhas_folha:
            i += 1
        else:
            print("--- // ---")
            i = 0
        print(colunas_centralizadas[h])
    if len(colunas_centralizadas) % linhas_folha != 0:
        numero_linhas = int(len(linhas_centralizadas) % linhas_folha)
        for l in range(numero_linhas):
            print()
        print("--- // ---")
    print("--- // ---")

def main():
    arquivo = input()
    segunda_linha = input().split(" ")
    caracteres_linha = int(segunda_linha[0])
    linhas_folha = int(segunda_linha[1])
    largura = int(input())
    with open(arquivo) as texto:
        blocos = texto.read()
        paragrafos_divididos = une_linhas(blocos)
        linhas_divididas = quebra_paragrafos(paragrafos_divididos, largura)
        linhas_centralizadas = centraliza_paragrafos(largura, linhas_divididas)
        paginas = divide_paginas(linhas_folha, linhas_centralizadas)
        colunas_centralizadas = cria_colunas(paginas, caracteres_linha, largura, linhas_folha)
        imprime_paginas(linhas_folha, colunas_centralizadas)

main()