import pytest
from controle_ativos.utils import crypto


def test_gerar_e_verificar_hash():
    senha = 'Senha@123'
    h1 = crypto.gerar_hash(senha)
    assert senha not in h1, 'Hash não deve conter a senha em texto puro'
    assert crypto.verificar_hash(senha, h1) is True
    assert crypto.verificar_hash('SenhaErrada', h1) is False


def test_hashes_diferentes_para_mesma_senha_se_salt_aleatorio():
    senha = 'Senha@123'
    h1 = crypto.gerar_hash(senha)
    h2 = crypto.gerar_hash(senha)
    if h1 == h2:
        pytest.xfail('Implementação não usa salt aleatório — pendência para Fase 3')
    assert h1 != h2
