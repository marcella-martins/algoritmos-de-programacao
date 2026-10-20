import json
from types import SimpleNamespace

# atualizando os indices em todas as funções
def criar_colecao():
    # FIXME: modifique conforme a sua descrição acima
    colecao = SimpleNamespace()
    colecao.artigos = {}
    colecao.indices = {}
    return colecao


def obter_nome_artigo(colecao, id_artigo):
    return colecao.artigos[id_artigo]["titulo"]


def carregar_arquivo(colecao, nome_arquivo):
    with open(nome_arquivo) as arquivo:
        lista_artigos = json.load(arquivo)
    # FIXME: carregue a lista de artigos lidos na sua coleção
    for artigo in lista_artigos:
        id_artigo = artigo["id"]
        colecao.artigos[id_artigo] = artigo
        for referencia in artigo["referencias"]:
            # para relacionar o id dos que citam o artigo
            if referencia not in colecao.indices:
                colecao.indices[referencia] = set()
            colecao.indices[referencia].add(id_artigo)


def obter_numero_artigos(colecao):
    return len(colecao.artigos)


def obter_palavras(colecao):
    # adiciona cada palavra-chave se não estiver na lista
    lista_palavras = []
    for artigo in colecao.artigos.values():
        sublista_palavras = artigo["palavras-chave"]
        for palavra in sublista_palavras:
            if not palavra in lista_palavras:
                lista_palavras.append(palavra)
    lista_palavras.sort()
    return lista_palavras


def obter_principais_autores(colecao):
    # lista todos, incluindo repetições
    autores = []
    for artigo in colecao.artigos.values():
        autores_artigo = artigo["autores"]
        for autor in autores_artigo:
            autores.append(autor)
    # cria um dict que relaciona um autor ao número de obras
    contagem = {}
    for autor in autores:
        if autor in contagem:
            contagem[autor] = contagem[autor] + 1
        else:
            contagem[autor] = 1
    # para casos de lista vazia
    if not contagem:
        return 0, []
    # roda a lista de autores procurando aqueles que têm maior número de obras
    maximo = max(contagem.values())
    principais_autores = []
    for autor, obras in contagem.items():
        if obras == maximo:
            principais_autores.append(autor)
    principais_autores.sort()
    return maximo, principais_autores


def obter_referencias_orfas(colecao):
    #procura presença das referencias dentro da coleção de artigos
    referencias_orfas = []
    for artigo in colecao.artigos.values():
        for referencia in artigo["referencias"]:
            if referencia not in colecao.artigos and referencia not in referencias_orfas:
                referencias_orfas.append(referencia)
    referencias_orfas.sort()
    return referencias_orfas


def buscar_citacoes(colecao, id_artigo):
    #cria lista de ids que citam outro artigo
    if id_artigo not in colecao.indices:
        return []
    return list(colecao.indices[id_artigo])


def buscar_palavras(colecao, consulta):
    ids_citantes = []
    for id_artigo, artigo in colecao.artigos.items():
        palavras_artigo = artigo["palavras-chave"]
        # any para OU e all para E, facilitando as comparações
        if any(all(palavra in palavras_artigo for palavra in conjuntos) for conjuntos in consulta):
            ids_citantes.append(id_artigo)
    return ids_citantes


def inserir_artigo(colecao, id_artigo, titulo, autores, ano, palavras, referencias):
    if id_artigo in colecao.artigos:
        return False
    colecao.artigos[id_artigo] = {
        "id": id_artigo,
        "titulo": titulo,
        "autores": autores,
        "ano": ano,
        "palavras-chave": sorted(palavras),
        "referencias": sorted(referencias)
    }
    for referencia in referencias:
        if referencia not in colecao.indices:
            colecao.indices[referencia] = set()
        colecao.indices[referencia].add(id_artigo)
    return True


def remover_artigo(colecao, id_artigo):
    if id_artigo not in colecao.artigos:
        return False
    referencias = colecao.artigos[id_artigo]["referencias"]
    for referencia in referencias:
        if referencia in colecao.indices:
            if id_artigo in colecao.indices[referencia]:
                colecao.indices[referencia].remove(id_artigo)
    del colecao.artigos[id_artigo]
    return True


def alterar_palavras(colecao, id_artigo, palavras_novas):
    if id_artigo not in colecao.artigos:
        return False
    colecao.artigos[id_artigo]["palavras-chave"] = sorted(palavras_novas)
    return True


def alterar_referencias(colecao, id_artigo, referencias_novas):
    if id_artigo not in colecao.artigos:
        return False
    referencias_antigas = colecao.artigos[id_artigo]["referencias"]
    for referencia in referencias_antigas:
        if referencia in colecao.indices:
            if id_artigo in colecao.indices[referencia]:
                colecao.indices[referencia].remove(id_artigo)
    colecao.artigos[id_artigo]["referencias"] = sorted(referencias_novas)
    for referencia in referencias_novas:
        if referencia not in colecao.indices:
            colecao.indices[referencia] = set()
        colecao.indices[referencia].add(id_artigo)
    return True


def gravar_arquivo(colecao, nome_arquivo):
    # FIXME: prepare uma lista de arquivos no formato do arquivo JSON
    lista_artigos = []
    for id_artigo in sorted(colecao.artigos):
        # dicionariza os dados, adicionando o id dentro do dict
        dados_artigo = colecao.artigos[id_artigo]
        artigo = dict(dados_artigo)
        artigo["id"] = id_artigo
        lista_artigos.append(artigo)
    with open(nome_arquivo, "w") as arquivo:
        json.dump(lista_artigos, arquivo, indent=2, ensure_ascii=False)
