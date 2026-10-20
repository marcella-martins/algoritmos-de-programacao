import telemetria


def mensagem_padrao(nome_da_funcao):
    return "Resultado errado na função " + nome_da_funcao


def teste_unidade_01_distancia():
    mensagem = mensagem_padrao("distancia")
    assert telemetria.distancia(0, 0, 3, 4) == 5.0, mensagem


def teste_unidade_02_detectar_corrompidas():
    mensagem = mensagem_padrao("detectar_corrompidas")
    leituras = [
        (0, 0.0, 0.0),
        (1, 1.0, 0.0),
        (2, 50.0, 0.0),
        (3, 3.0, 0.0),
        (4, 4.0, 0.0),
    ]
    v_max = 2.0
    resultado = telemetria.detectar_corrompidas(leituras, v_max)
    assert resultado == [False, False, True, False, False], mensagem


def teste_unidade_03_interpolar():
    mensagem = mensagem_padrao("interpolar")
    x, y = telemetria.interpolar(0, 0, 0, 10, 10, 4, 2)
    assert x == 5.0, mensagem
    assert y == 5.0, mensagem


def teste_unidade_04_reconstruir():
    mensagem = mensagem_padrao("reconstruir")

    leituras = [
        (0, 0.0, 0.0),
        (1, 100.0, 100.0),
        (2, 2.0, 2.0),
    ]
    corrompidas = [False, True, False]
    corrigida = telemetria.reconstruir(leituras, corrompidas)
    assert corrigida[1] == (1, 1.0, 1.0), mensagem

    leituras = [
        (0, 0.0, 0.0),
        (1, 100.0, 100.0),
        (2, 50.0, 50.0),
        (3, 200, 0),
    ]
    corrompidas = [False, False, True, False]
    corrigida = telemetria.reconstruir(leituras, corrompidas)
    assert corrigida[2] == (2, 150.0, 50.0), mensagem


def teste_unidade_05_max_variacao():
    mensagem = mensagem_padrao("max_variacao")
    assert telemetria.max_variacao([1.0, 3.0, 2.0, 5.0]) == 3.0, mensagem
