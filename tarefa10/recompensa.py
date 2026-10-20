def ler_entrada():
    n, x = input().split()
    return int(n), int(x)


def calcular_probabilidade(n, x):
    if n == 0:
        return 0
    chances = 0
    for face in range(1,7):
        if face == x:
            chances += 1/6
        elif face < x:
            chances += 1/6 * calcular_probabilidade(n - 1, x - face)
    # loop for que indica a soma de probabilidade de joão ganhar, considerando que face > x não dá nada
    return chances


def main():
    n, x = ler_entrada()
    probabilidade_recompensa = calcular_probabilidade(n, x)
    print(f"{probabilidade_recompensa:.3f}")


main()