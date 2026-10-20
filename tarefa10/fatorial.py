def ler_entrada():
    numero = input()
    return int(numero)


def fatorial(numero):
    if numero == 0 or numero == 1:
        numero_fatorial = 1
    else:
        numero_fatorial = numero * fatorial(numero - 1)
    return numero_fatorial


def main():
    numero = ler_entrada()
    numero_fatorial = fatorial(numero)
    print(numero_fatorial)


main()