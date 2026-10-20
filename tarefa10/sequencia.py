def ler_entrada():
    numero = int(input())
    return numero


def calcular_numero(n, t):
    if t[n] is None:
        if n == 1:
            t[n] = 1
        elif n == 2:
            t[n] = 2
        elif n == 3:
            t[n] = 3
        else:
            t[n] = calcular_numero(n - 1, t) + 2 * calcular_numero(n - 2, t) + 3 * calcular_numero(n - 3, t)
    return t[n]


def main():
    numero = ler_entrada()
    t = [None] * (numero + 1)
    enesimo_numero = calcular_numero(numero, t)
    print(enesimo_numero)


main()