import math
def ler_trajetoria():
    """
    Lê os dados de telemetria da entrada padrão.
    A entrada contém o número N de leituras, a velocidade máxima V_max
    e N linhas com instante t, coordenada x e coordenada y.
    Devolve a velocidade máxima e uma lista de tuplas (t, x, y).

    Exemplo de uso: v_max, leituras = ler_trajetoria()
    """
    n = int(input())
    v_max = float(input())
    leituras = []
    for i in range(0, n):
        linha = input().split()
        tuplas = (float(linha[0]), float(linha[1]), float(linha[2]))
        leituras.append(tuplas)
    return v_max, leituras


def distancia(x1, y1, x2, y2):
    """
    Recebe as coordenadas de dois pontos (x1, y1) e (x2, y2).
    Devolve a distância euclidiana entre eles.

    Exemplo: distancia(0, 0, 3, 4) devolve 5.0.
    """
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia



def detectar_corrompidas(leituras, v_max):
    """
    Recebe uma lista de tuplas (t, x, y) representando as leituras
    de telemetria e a velocidade máxima da sonda.
    Devolve uma lista de booleanos de mesmo tamanho, onde True
    indica que a leitura correspondente é corrompida.
    A primeira e a última leitura são sempre válidas (False).

    Exemplo de uso: corrompidas = detectar_corrompidas(leituras, v_max)
    """
    corrompidas = []
    i_valido = 0
    for i in range(0, len(leituras)):
        if i == 0 or i == len(leituras) - 1:
            corrompidas.append(False)
        else:
            t_v, x_v, y_v = leituras[i_valido]
            t_a, x_a, y_a = leituras[i]
            v_med = (math.sqrt((x_a - x_v)**2 + (y_a - y_v)**2)) / (t_a - t_v)
            if v_med > v_max:
                corrompidas.append(True)
            else:
                corrompidas.append(False)
                i_valido = i
    return corrompidas


def interpolar(xa, ya, ta, xb, yb, tb, t):
    """
    Recebe as coordenadas e instantes de dois pontos válidos
    (xa, ya) no instante ta e (xb, yb) no instante tb,
    e o instante t de uma leitura corrompida (ta < t < tb).
    Devolve um par x, y com as coordenadas interpoladas.

    Exemplo: interpolar(0, 0, 0, 10, 10, 4, 2) devolve 5.0, 5.0.
    """
    x_interpolar = xa + ((xb - xa) * (t - ta) / (tb - ta))
    y_interpolar = ya + ((yb - ya) * (t - ta) / (tb - ta))
    return x_interpolar, y_interpolar


def reconstruir(leituras, corrompidas):
    """
    Recebe uma lista de tuplas (t, x, y) representando as leituras
    de telemetria e uma lista de booleanos indicando quais leituras
    são corrompidas.
    Devolve uma nova lista de tuplas (t, x, y) com a trajetória
    corrigida, substituindo leituras corrompidas por valores
    interpolados.

    Exemplo de uso: corrigida = reconstruir(leituras, corrompidas)
    """
    corrigida = []
    for i in range(0, len(leituras)):
        t_at, x_at, y_at = leituras[i]
        if not corrompidas[i]:
            corrigida.append((t_at, x_at, y_at))
        else:
            t_an, x_an, y_an = corrigida[i-1]
            j = i + 1
            while j < len(corrompidas) and corrompidas[j] == True:
                j += 1
            t_pr, x_pr, y_pr = leituras[j]
            x_n, y_n = interpolar(x_an, y_an, t_an, x_pr, y_pr, t_pr, t_at)
            corrigida.append((t_at, x_n, y_n))
    return corrigida


def max_variacao(valores):
    """
    Recebe uma lista de números (com pelo menos dois elementos).
    Devolve a maior diferença absoluta entre dois elementos
    consecutivos da lista.

    Exemplo: max_variacao([1.0, 3.0, 2.0, 5.0]) devolve 3.0,
    pois |5.0 - 2.0| = 3.0 é a maior variação consecutiva.
    """
    max_variacao = 0.0
    for i in range(0, len(valores)-1):
        val_atual = math.sqrt((valores[i+1] - valores[i])**2)
        if val_atual > max_variacao:
            max_variacao = val_atual
    return max_variacao