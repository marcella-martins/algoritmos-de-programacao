from telemetria import ler_trajetoria, distancia, detectar_corrompidas, interpolar, reconstruir, max_variacao
def calcular_metricas(corrigida):
    distancia_total = 0
    velocidade_maxima = 0
    velocidades = []
    for i in range(0, len(corrigida) - 1):
        a = corrigida[i]
        b = corrigida[i+1]
        distancia_atual = distancia(a[1], a[2], b[1], b[2])
        distancia_total += distancia_atual
        velocidade_atual = distancia_atual / (b[0] - a[0])
        velocidades.append(velocidade_atual)
        if velocidade_atual > velocidade_maxima:
            velocidade_maxima = velocidade_atual
    return distancia_total, velocidade_maxima, velocidades  
def proxima_posicao(corrigida): 
    #tinha tentado colocar como parâmetro corrigida[-1], corrigida[-2], porém, o teste não funcionou
    x_proximo = corrigida[-1][1] + (corrigida[-1][1] - corrigida[-2][1])
    y_proximo = corrigida[-1][2] + (corrigida[-1][2] - corrigida[-2][2])
    return x_proximo, y_proximo
def main():
    v_max, leituras = ler_trajetoria()
    destino = input().split()
    x_destino, y_destino = float(destino[0]), float(destino[1])
    corrompidas = detectar_corrompidas(leituras, v_max)
    corrigida = reconstruir(leituras, corrompidas)
    distancia_total, velocidade_maxima, velocidades = calcular_metricas(corrigida)
    distancia_partida = distancia(corrigida[0][1], corrigida[0][2], corrigida[-1][1], corrigida[-1][2])
    variacao_maxima = max_variacao(velocidades)
    distancia_destino = distancia(corrigida[-1][1], corrigida[-1][2], x_destino, y_destino)
    x_proximo, y_proximo = proxima_posicao(corrigida)
    print(f"Distância total percorrida: {distancia_total:.2f} \nDistância ao ponto de partida: {distancia_partida:.2f} \nVelocidade máxima: {velocidade_maxima:.2f} \nVariação máxima de velocidade: {variacao_maxima:.2f} \nDistância ao destino: {distancia_destino:.2f} \nPróxima posição estimada: {x_proximo:.2f} {y_proximo:.2f}")
main()
