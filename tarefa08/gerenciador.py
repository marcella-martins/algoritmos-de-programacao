"""
Você NÃO deve alterar esse arquivo!

Leia e estude o programa abaixo com bastante cuidado para
saber como as funções do arquivo artigos.py são chamadas.

Você deve modificar e completar o arquivo artigos.py.
"""

import artigos


def dividir_texto(texto, separador):
    return [parte.strip() for parte in texto.split(separador)]


def mostrar_lista(titulo, lista):
    print(f"{titulo}:")
    for item in lista:
        print(f" - {item}")


def mostrar_lista_artigos(colecao, titulo, ids_artigo):
    linhas = []
    for id_artigo in sorted(ids_artigo):
        nome_artigo = artigos.obter_nome_artigo(colecao, id_artigo)
        linha = f"{id_artigo}: {nome_artigo}"
        linhas.append(linha)
    mostrar_lista(titulo, linhas)


def processar_carregar_arquivo(colecao, parametros):
    nome_arquivo = parametros
    try:
        artigos.carregar_arquivo(colecao, nome_arquivo)
        ok = True
    except IOError:
        ok = False
    if ok:
        print(f"Artigos de {nome_arquivo} carregados")
    else:
        print(f"Não foi possível carregar {nome_arquivo}")


def processar_descrever_colecao(colecao, parametros):
    numero_artigos = artigos.obter_numero_artigos(colecao)
    palavras = artigos.obter_palavras(colecao)
    numero, principal_autores = artigos.obter_principais_autores(colecao)
    referencias_orfas = artigos.obter_referencias_orfas(colecao)

    print(f"A coleção contém {numero_artigos} artigos")
    print()
    mostrar_lista("Lista de palavras-chave", palavras)
    print()
    mostrar_lista(f"Autores com mais publicações ({numero} artigos)", principal_autores)
    print()
    mostrar_lista("Referências órfãs", referencias_orfas)


def processar_buscar_citacoes(colecao, parametros):
    ids_str = parametros.split()
    for id_str in ids_str:
        id_artigo = int(id_str)
        lista_artigos = artigos.buscar_citacoes(colecao, id_artigo)
        mostrar_lista_artigos(colecao, f"Citações de {id_artigo}", lista_artigos)


def processar_buscar_palavras(colecao, parametros):
    consulta = []
    for parte in dividir_texto(parametros, "|"):
        palavras = [p.strip() for p in dividir_texto(parte, "+")]
        consulta.append(palavras)
    lista_artigos = artigos.buscar_palavras(colecao, consulta)
    mostrar_lista_artigos(colecao, f"Busca por {parametros}", lista_artigos)


def processar_inserir_artigo(colecao, parametros):
    partes = dividir_texto(parametros, ";")
    assert len(partes) == 6, "formato inválido"
    id_artigo = int(partes[0])
    titulo = partes[1]
    autores = dividir_texto(partes[2], ",")
    ano = int(partes[3])
    palavras = dividir_texto(partes[4], ",")
    referencias = [int(ref_str) for ref_str in dividir_texto(partes[5], ",") if ref_str != ""]
    ok = artigos.inserir_artigo(colecao, id_artigo, titulo, autores, ano, palavras, referencias)
    if ok:
        print(f"Artigo {id_artigo} inserido")
    else:
        print(f"Artigo {id_artigo} já existe")


def processar_remover_artigo(colecao, parametros):
    id_artigo = int(parametros)
    ok = artigos.remover_artigo(colecao, id_artigo)
    if ok:
        print(f"Artigo {id_artigo} removido")
    else:
        print(f"Artigo {id_artigo} não existe")


def processar_alterar_palavras(colecao, parametros):
    partes = dividir_texto(parametros, ";")
    assert len(partes) == 2, "formato inválido"
    id_artigo = int(partes[0])
    palavras = dividir_texto(partes[1], ",")
    ok = artigos.alterar_palavras(colecao, id_artigo, palavras)
    if ok:
        print(f"Palavras-chave do artigo {id_artigo} alteradas")
    else:
        print(f"Artigo {id_artigo} não existe")


def processar_alterar_referencias(colecao, parametros):
    partes = dividir_texto(parametros, ";")
    assert len(partes) == 2, "formato inválido"
    id_artigo = int(partes[0])
    referencias = [int(ref_str) for ref_str in dividir_texto(partes[1], ",") if ref_str != ""]
    ok = artigos.alterar_referencias(colecao, id_artigo, referencias)
    if ok:
        print(f"Referências do artigo {id_artigo} alteradas")
    else:
        print(f"Artigo {id_artigo} não existe")


def processar_gravar_arquivo(colecao, parametros):
    nome_arquivo = parametros
    try:
        artigos.gravar_arquivo(colecao, nome_arquivo)
        ok = True
    except IOError:
        ok = False
    if ok:
        print(f"Dados gravados em  {nome_arquivo}")
    else:
        print(f"Não foi possível criar {nome_arquivo}")


def main():
    colecao = artigos.criar_colecao()

    mapa_operacoes = {
        "CARREGAR-ARQUIVO": processar_carregar_arquivo,
        "DESCREVER-COLECAO": processar_descrever_colecao,
        "BUSCAR-CITACOES": processar_buscar_citacoes,
        "BUSCAR-PALAVRAS": processar_buscar_palavras,
        "INSERIR-ARTIGO": processar_inserir_artigo,
        "REMOVER-ARTIGO": processar_remover_artigo,
        "ALTERAR-PALAVRAS": processar_alterar_palavras,
        "ALTERAR-REFERENCIAS": processar_alterar_referencias,
        "GRAVAR-ARQUIVO": processar_gravar_arquivo,
    }

    while True:
        try:
            linha = input()
        except EOFError:
            break
        operacao, parametros = linha.split(":", maxsplit=1)
        parametros = parametros.strip()
        if operacao in mapa_operacoes:
            processar_operacao = mapa_operacoes[operacao]
            processar_operacao(colecao, parametros)
            print()
        else:
            print(f"Operação {operacao} não reconhecida")


main()
