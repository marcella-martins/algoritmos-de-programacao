def ler_entrada():
    a, b = input().split()
    return int(a), int(b)


def descobrir_mdc(a, b):
    if b == 0:
        return a
    else:
        return descobrir_mdc(b, a % b)


def main():
    a, b = ler_entrada()
    maximo_divisor = descobrir_mdc(a, b)
    print(maximo_divisor)


main()