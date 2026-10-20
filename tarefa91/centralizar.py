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
    proximo_paragrafo = paragrafos
    while len(proximo_paragrafo) > 0:
        if proximo_paragrafo[0] == " ":
            proximo_paragrafo = proximo_paragrafo[1:]
        for i in range(largura, -1, -1):
            if len(proximo_paragrafo) - 1 >= i:
                if proximo_paragrafo[i] == " ":
                    if i == largura:
                        paragrafos_quebrados.append(proximo_paragrafo[0:i])
                        proximo_paragrafo = proximo_paragrafo[i:]
                    else:
                        paragrafos_quebrados.append(proximo_paragrafo[0:i + 1])
                        proximo_paragrafo = proximo_paragrafo[i + 1:]
                    break
            else:
                paragrafos_quebrados.append(proximo_paragrafo)
                proximo_paragrafo = []
                break
    return paragrafos_quebrados

def centraliza_paragrafos(largura, paragrafos_quebrados):
    paragrafos_atualizados = paragrafos_quebrados
    for a in range(len(paragrafos_atualizados)):
        for j in range(((largura - len(paragrafos_atualizados[a])) // 2)):
            paragrafos_atualizados[a] = " " + paragrafos_atualizados[a] + " "
        if (largura - len(paragrafos_atualizados[a])) % 2 != 0:
            if paragrafos_atualizados[a][-1] != " ":
                paragrafos_atualizados[a] += " "
            else:
                paragrafos_atualizados[a] = " " + paragrafos_atualizados[a]
    return paragrafos_atualizados

def imprime_paragrafos(paragrafos_atualizados):
    for b in range(len(paragrafos_atualizados)):
        print(paragrafos_atualizados[b])

def main():
    arquivo = input()
    largura = int(input())
    with open(arquivo) as texto:
        blocos = texto.read()
        paragrafos = une_linhas(blocos)
        for k in range(len(paragrafos)):
            paragrafos_quebrados = quebra_paragrafos(paragrafos[k], largura)
            paragrafos_atualizados = centraliza_paragrafos(largura, paragrafos_quebrados)
            imprime_paragrafos(paragrafos_atualizados)
            if len(paragrafos) > 1:
                print()
                
main()
