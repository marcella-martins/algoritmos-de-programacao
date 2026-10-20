from telemetria import ler_trajetoria, detectar_corrompidas, reconstruir
def imprimir(corrigida):
    for t, x, y in corrigida:
        print(f"{int(t)} {x:.2f} {y:.2f}")    
def main():
    v_max, leituras = ler_trajetoria()
    corrompidas = detectar_corrompidas(leituras, v_max)
    corrigida = reconstruir(leituras, corrompidas)
    imprimir(corrigida)
main()