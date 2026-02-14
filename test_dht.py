"""
7 Casos de Teste — Arkham Asylum DHT
Executar: python -m pytest test_dht.py -v
"""
from dht import ArkhamDHT


def criar_arkham(m, alas):
    dht = ArkhamDHT(m)
    for a in alas:
        dht.construir_ala(a)
    return dht


# Teste 1 — Internar e Localizar o Coringa
# Pré: Arkham com 3 alas, vazio
# Etapas: internar Coringa e Hera, localizar ambos
# Pós: fichas retornadas corretamente
def test_internar_e_localizar():
    ark = criar_arkham(3, [1, 3, 6])
    ark.internar("Coringa", {"crime": "terrorismo", "perigo": 10})
    ark.internar("Hera Venenosa", {"crime": "ecoterrorismo", "perigo": 7})
    assert ark.localizar("Coringa")["perigo"] == 10
    assert ark.localizar("Hera Venenosa")["crime"] == "ecoterrorismo"


# Teste 2 — Fuga do Espantalho
# Pré: Espantalho internado
# Etapas: registrar fuga, tentar localizar
# Pós: fuga=True, localizar=None, segunda fuga=False
def test_fuga():
    ark = criar_arkham(3, [1, 3, 6])
    ark.internar("Espantalho", {"crime": "uso de toxinas", "perigo": 8})
    assert ark.registrar_fuga("Espantalho") is True
    assert ark.localizar("Espantalho") is None
    assert ark.registrar_fuga("Espantalho") is False


# Teste 3 — Nova ala construída, redistribuição de vilões
# Pré: 2 alas com 5 vilões internados
# Etapas: construir 3ª ala, localizar todos
# Pós: todos acessíveis, 3 alas ativas
def test_nova_ala():
    ark = criar_arkham(4, [4, 12])
    viloes = ["Coringa", "Bane", "Riddler", "Pinguim", "Duas-Caras"]
    for v in viloes:
        ark.internar(v, {"nome": v})
    ark.construir_ala(8)
    assert len(ark.alas) == 3
    for v in viloes:
        assert ark.localizar(v) is not None, f"{v} desapareceu!"


# Teste 4 — Ala destruída pelo Bane, migração de prisioneiros
# Pré: 3 alas com 6 vilões
# Etapas: interditar 1 ala, localizar todos
# Pós: 2 alas, nenhum vilão perdido
def test_ala_interditada():
    ark = criar_arkham(4, [3, 8, 13])
    viloes = ["Coringa", "Bane", "Hera Venenosa", "Espantalho", "Mr. Freeze", "Riddler"]
    for v in viloes:
        ark.internar(v, {"nome": v})
    ark.interditar_ala(8)
    assert len(ark.alas) == 2
    for v in viloes:
        assert ark.localizar(v) is not None, f"{v} perdido!"


# Teste 5 — Internação em massa, todos localizáveis
# Pré: 4 alas, vazio
# Etapas: internar 20 vilões, localizar todos
# Pós: 100% encontrados, distribuídos em ≥2 alas
def test_internacao_em_massa():
    ark = criar_arkham(8, [30, 90, 150, 210])
    viloes = {f"Vilão_{i}": {"id": i} for i in range(20)}
    for nome, ficha in viloes.items():
        ark.internar(nome, ficha)
    for nome in viloes:
        assert ark.localizar(nome) is not None
    assert sum(1 for a in ark.alas if a.prisioneiros) >= 2


# Teste 6 — Atualizar ficha (vilão muda de nível de perigo)
# Pré: Coringa internado com perigo=8
# Etapas: atualizar ficha para perigo=10
# Pós: localizar retorna ficha atualizada
def test_atualizar_ficha():
    ark = criar_arkham(3, [1, 3, 6])
    ark.internar("Coringa", {"crime": "roubo", "perigo": 8})
    ark.internar("Coringa", {"crime": "terrorismo", "perigo": 10})
    ficha = ark.localizar("Coringa")
    assert ficha["perigo"] == 10
    assert ficha["crime"] == "terrorismo"


# Teste 7 — Buscar vilão que nunca foi internado
# Pré: Arkham com 3 alas, vazio
# Etapas: localizar "Batman"
# Pós: retorna None
def test_vilao_inexistente():
    ark = criar_arkham(3, [1, 3, 6])
    assert ark.localizar("Batman") is None
