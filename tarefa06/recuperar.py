def organizar_alteradas(arquivo):
    vendas = []
    with open(arquivo) as alteradas:
        for linha in alteradas:
            hora_venda, codigo_venda, categoria, valor = linha.strip().split(",")
            vendas.append((hora_venda, int(codigo_venda), categoria, float(valor)))
    return vendas
def organizar_subtotais(arquivo):
    logs = []
    with open(arquivo) as subtotais:
        for horizontal in subtotais:
            horas, estoque_dinossauros, estoque_carros, valor_total = horizontal.strip().split(",")
            logs.append((horas, int(estoque_dinossauros), int(estoque_carros), float(valor_total)))
    return logs
def corrigir_categorias(logs):
    corrigidas = []
    for i in range(1, len(logs)):
        anterior = logs[i - 1]
        atual = logs[i]
        hora = atual[0]
        if atual[1] < anterior[1]:
            categoria = "dinossauro"
        else:
            categoria = "carro"
        valor_compra = round(atual[3] - anterior[3], 2)
        corrigidas.append((hora, categoria, valor_compra))
    return corrigidas
def comparar(vendas, corrigidas):
    """não consegui reduzir as funções, porque aí encontrava um novo erro"""
    horas = []
    codigos = []
    categorias = []
    valores = []
    for a in vendas:
        horas.append(a[0])
        codigos.append(a[1])
        categorias.append(a[2])
        valores.append(a[3])
    deletadas = []
    indice = 1
    b = 0
    while b < len(corrigidas):
        hora = corrigidas[b][0]
        brinquedo = corrigidas[b][1]
        preco = corrigidas[b][2]
        if indice < len(horas) and hora == horas[indice] and brinquedo == categorias[indice]:
            contagem_log = 0
            for k in range(b, len(corrigidas)):
                if corrigidas[k][0] == hora and corrigidas[k][1] == brinquedo:
                    contagem_log += 1
                else:
                    break
            contagem_venda = 0
            for k in range(indice, len(horas)):
                if horas[k] == hora and categorias[k] == brinquedo:
                    contagem_venda += 1
                else:
                    break
            if contagem_log > contagem_venda:
                valores_venda = []
                for k in range(indice, indice + contagem_venda):
                    valores_venda.append(valores[k])
                for i in range(contagem_log):
                    valor_log = corrigidas[b + i][2]
                    if valor_log in valores_venda:
                        valores_venda.remove(valor_log)
                    else:
                        if i < contagem_venda:
                            codigo_anterior = codigos[indice - 1]
                            codigo_proximo  = codigos[indice + 1]
                        else:
                            codigo_anterior = codigos[indice + contagem_venda - 1]
                            if indice + contagem_venda < len(codigos):
                                codigo_proximo = codigos[indice + contagem_venda]
                            else:
                                codigo_proximo = None
                        deletadas.append((corrigidas[b + i][0], corrigidas[b + i][1], corrigidas[b + i][2], codigo_anterior, codigo_proximo))
            indice += contagem_venda
            b += contagem_log
        else:
            codigo_anterior = codigos[indice - 1]
            if indice < len(codigos):
                codigo_proximo = codigos[indice]
            else:
                codigo_proximo = None
            deletadas.append((hora, brinquedo, preco, codigo_anterior, codigo_proximo))
            b += 1
    return deletadas
def codigo_engracado(numero):
    num = str(numero)
    tamanho = len(num)
    for c in range(1, tamanho // 2 + 1):
        if tamanho % c == 0:
            bloco = num[:c]
            if bloco * (tamanho // c) == num:
                return True
    return False
def encontrar_codigo(codigo_anterior, codigo_proximo, codigos_atualizados):
    if codigo_anterior != None:
        if codigo_proximo != None:
            for e in range(codigo_anterior + 1, codigo_proximo):
                if codigo_engracado(e) and e not in codigos_atualizados:
                    codigos_atualizados.append(e)
                    return e
        else:
            codigo = codigo_anterior + 1
            while True:
                if codigo_engracado(codigo) and codigo not in codigos_atualizados:
                    codigos_atualizados.append(codigo)
                    return codigo
                codigo += 1
    return None
def main():
###categoria final esta a mais se repetindo
    arquivo_vendas = input()
    arquivo_logs = input()
    vendas = organizar_alteradas(arquivo_vendas)
    logs = organizar_subtotais(arquivo_logs)
    corrigidas = corrigir_categorias(logs)
    deletadas = comparar(vendas, corrigidas)
    codigos_atualizados = []
    for g in deletadas:
        codigo = encontrar_codigo(g[3], g[4], codigos_atualizados)
        print(f"{g[0]},{codigo},{g[1]},{g[2]:.2f}")
main()
