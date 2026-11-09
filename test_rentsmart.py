import unittest

from main import Apartamento, Casa, Estudio, Locacao, TaxaContratual


class TestOrcamento(unittest.TestCase):
    def test_apto_1q_sem_garagem_sem_criancas_tem_desconto(self):
        loc = Locacao(Apartamento(1, 0), False, TaxaContratual(1))
        self.assertEqual(loc.aluguel_mensal(), 665.00)

    def test_apto_2q_garagem_sem_criancas(self):
        loc = Locacao(Apartamento(2, 1), False, TaxaContratual(1))
        self.assertEqual(loc.aluguel_mensal(), 1140.00)

    def test_apto_2q_garagem_com_criancas_sem_desconto(self):
        loc = Locacao(Apartamento(2, 1), True, TaxaContratual(1))
        self.assertEqual(loc.aluguel_mensal(), 1200.00)

    def test_casa_2q_garagem(self):
        loc = Locacao(Casa(2, 1), False, TaxaContratual(1))
        self.assertEqual(loc.aluguel_mensal(), 1450.00)

    def test_casa_1q_sem_garagem(self):
        loc = Locacao(Casa(1, 0), False, TaxaContratual(1))
        self.assertEqual(loc.aluguel_mensal(), 900.00)

    def test_estudio_vagas(self):
        self.assertEqual(Estudio(0).valor_vagas(), 0)
        self.assertEqual(Estudio(2).valor_vagas(), 250.00)
        self.assertEqual(Estudio(3).valor_vagas(), 310.00)
        self.assertEqual(Estudio(4).valor_vagas(), 370.00)

    def test_estudio_nao_tem_desconto(self):
        loc = Locacao(Estudio(0), False, TaxaContratual(1))
        self.assertEqual(loc.aluguel_mensal(), 1200.00)


class TestTaxa(unittest.TestCase):
    def test_parcelas_3x(self):
        t = TaxaContratual(3)
        self.assertEqual(t.valor_no_mes(1), 666.67)
        self.assertEqual(t.valor_no_mes(2), 666.67)
        self.assertEqual(t.valor_no_mes(3), 666.66)
        self.assertEqual(t.valor_no_mes(4), 0)

    def test_soma_parcelas_fecha_2000(self):
        for n in range(1, 6):
            t = TaxaContratual(n)
            total = round(sum(t.valor_no_mes(m) for m in range(1, 13)), 2)
            self.assertEqual(total, 2000.00)


if __name__ == "__main__":
    unittest.main()
