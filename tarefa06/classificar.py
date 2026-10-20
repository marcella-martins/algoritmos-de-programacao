def organizar_vendas(arquivo):
    horas = []
    categorias = []
    valores = []
    with open(arquivo) as vendas:
        for linha in vendas:
            hora_venda, codigo_venda, categoria, valor = linha.strip().split(",")
            horas.append(hora_venda)
            categorias.append(categoria)
            valores.append(float(valor))
    return horas, categorias, valores
def diferenciar_categorias(horas, categorias, valores):
    horas_carro = []
    valores_carro = []
    horas_dinossauro = []
    valores_dinossauro = []
    for i in range(len(categorias)):
        hora_inteira = horas[i][:2] + "h"
        if categorias[i] == "carro":
            horas_carro.append(hora_inteira)
            valores_carro.append(valores[i])
        elif categorias[i] == "dinossauro":
            horas_dinossauro.append(hora_inteira)
            valores_dinossauro.append(valores[i])
    return horas_carro, valores_carro, horas_dinossauro, valores_dinossauro
def diferenciar_horarios(horas_categoria, valores_categoria):
    hora_unica = []
    total = []
    for i in range(len(horas_categoria)):
        hora = horas_categoria[i]
        valor = valores_categoria[i]
        encontrada = False
        for j in range(len(hora_unica)):
            if hora_unica[j] == hora:
                total[j] += valor
                encontrada = True
                break
        if not encontrada:
            hora_unica.append(hora)
            total.append(valor)
    return hora_unica, total
def resultado (hora, total):
    for i in range(len(total)):
        maior = i
        for j in range(i+1, len(total)):
            if total[j] > total[maior]:
                maior = j
            elif total[j] == total[maior]:
                if hora[j] < hora[maior]:
                    maior = j
        total[i], total[maior] = total[maior], total[i]
        hora[i], hora[maior] = hora[maior], hora[i]
    return hora, total
def imprimir(nome, hora, total):
    print(nome + ":")
    for i in range(len(hora)):
        print(f"{hora[i]}: {total[i]:.2f}")
def main():
    try:
        arquivo = input()
        horas, categorias, valores = organizar_vendas(arquivo)
        horas_carro, valores_carro, horas_dinossauro, valores_dinossauro = diferenciar_categorias(horas, categorias, valores)
        horas_carro, totais_carro = diferenciar_horarios(horas_carro, valores_carro)
        horas_dinossauro, totais_dinossauro = diferenciar_horarios(horas_dinossauro, valores_dinossauro)
        horas_carro, totais_carro = resultado(horas_carro, totais_carro)
        horas_dinossauro, totais_dinossauro = resultado(horas_dinossauro, totais_dinossauro)
        imprimir("Carros", horas_carro, totais_carro)
        print()
        imprimir("Dinossauros", horas_dinossauro, totais_dinossauro)
    except EOFError:
        pass
main()      
