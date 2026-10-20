def ler_entrada():
    n, k = input().split()
    return int(n), int(k)


def calcular_coeficiente(n, k, par):
    if (n, k) not in par:
        if k == n or k == 0:
            par[(n, k)] = 1
        else:
            par[(n, k)] = calcular_coeficiente(n - 1, k - 1, par) + calcular_coeficiente(n - 1, k, par)
    return par[(n, k)]


def main():
    n, k = ler_entrada()
    par = {}
    coeficiente = calcular_coeficiente(n, k, par)
    print(coeficiente)


main()