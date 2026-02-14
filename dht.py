"""
Arkham Asylum DHT — Sistema de Gestão de Prisioneiros.
Distribui vilões entre as alas do asilo usando Consistent Hashing.
"""
import hashlib


class Ala:
    """Uma ala (nó) do Arkham Asylum."""
    def __init__(self, ala_id):
        self.ala_id = ala_id
        self.prisioneiros = {}  # nome_vilao -> ficha

    def __repr__(self):
        nomes = list(self.prisioneiros.keys())
        return f"Ala {self.ala_id}: {nomes if nomes else 'vazia'}"


class ArkhamDHT:
    """DHT com Consistent Hashing — cada ala cuida de um trecho do anel."""

    def __init__(self, m=4):
        self.size = 2 ** m
        self.alas = []

    def _hash(self, nome):
        """Calcula a posição do vilão no anel."""
        return int(hashlib.sha1(nome.encode()).hexdigest(), 16) % self.size

    def _ala_responsavel(self, nome):
        """Primeira ala com ID >= hash do nome (sentido horário)."""
        h = self._hash(nome)
        for ala in self.alas:
            if ala.ala_id >= h:
                return ala
        return self.alas[0]

    def construir_ala(self, ala_id):
        """Constrói nova ala e redistribui prisioneiros."""
        nova = Ala(ala_id)
        self.alas.append(nova)
        self.alas.sort(key=lambda a: a.ala_id)
        if len(self.alas) > 1:
            suc = self.alas[(self.alas.index(nova) + 1) % len(self.alas)]
            for nome in [n for n in suc.prisioneiros if self._ala_responsavel(n) == nova]:
                nova.prisioneiros[nome] = suc.prisioneiros.pop(nome)

    def interditar_ala(self, ala_id):
        """Interdita ala e transfere prisioneiros para a próxima."""
        ala = next(a for a in self.alas if a.ala_id == ala_id)
        suc = self.alas[(self.alas.index(ala) + 1) % len(self.alas)]
        suc.prisioneiros.update(ala.prisioneiros)
        self.alas.remove(ala)

    def internar(self, nome, ficha):
        """Interna vilão na ala responsável."""
        self._ala_responsavel(nome).prisioneiros[nome] = ficha

    def localizar(self, nome):
        """Localiza vilão. Retorna ficha ou None."""
        if not self.alas:
            return None
        return self._ala_responsavel(nome).prisioneiros.get(nome)

    def registrar_fuga(self, nome):
        """Registra fuga de vilão. Retorna True se estava internado."""
        ala = self._ala_responsavel(nome)
        return ala.prisioneiros.pop(nome, None) is not None

    def status(self):
        """Mostra estado do asilo."""
        print(f"\n🏚️ ARKHAM ASYLUM — {len(self.alas)} alas ativas")
        for ala in self.alas:
            print(f"  {ala}")
        print()
