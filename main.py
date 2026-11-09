# RentSmart - sistema de orcamento de locacao da R.M Imoveis
# Trabalho de Algoritmos e POO

import csv
import os


# ---------- classes dos imoveis ----------

class Imovel:
    def __init__(self, quartos, vagas):
        self.quartos = quartos
        self.vagas = vagas

    def valor_base(self):
        return 0

    def valor_quarto_extra(self):
        return 0

    def valor_vagas(self):
        return 0

    def tem_desconto_sem_criancas(self):
        return False

    def nome(self):
        return "Imovel"


class Apartamento(Imovel):
    def valor_base(self):
        return 700.00

    def valor_quarto_extra(self):
        if self.quartos == 2:
            return 200.00
        return 0

    def valor_vagas(self):
        return self.vagas * 300.00

    def tem_desconto_sem_criancas(self):
        return True

    def nome(self):
        return "Apartamento com %d quarto(s)" % self.quartos


class Casa(Imovel):
    def valor_base(self):
        return 900.00

    def valor_quarto_extra(self):
        if self.quartos == 2:
            return 250.00
        return 0

    def valor_vagas(self):
        return self.vagas * 300.00

    def nome(self):
        return "Casa com %d quarto(s)" % self.quartos


class Estudio(Imovel):
    def __init__(self, vagas):
        Imovel.__init__(self, 0, vagas)

    def valor_base(self):
        return 1200.00

    def valor_vagas(self):
        if self.vagas == 0:
            return 0
        extras = self.vagas - 2
        return 250.00 + extras * 60.00

    def nome(self):
        return "Estudio"


# ---------- taxa contratual ----------

class TaxaContratual:
    VALOR = 2000.00

    def __init__(self, parcelas):
        self.parcelas = parcelas

    def valor_parcela(self):
        return round(self.VALOR / self.parcelas, 2)

    def valor_no_mes(self, mes):
        if mes <= self.parcelas:
            if mes == self.parcelas:
                # ultima parcela ajusta os centavos
                return round(self.VALOR - self.valor_parcela() * (self.parcelas - 1), 2)
            return self.valor_parcela()
        return 0


# ---------- locacao (orcamento) ----------

class Locacao:
    def __init__(self, imovel, tem_criancas, taxa):
        self.imovel = imovel
        self.tem_criancas = tem_criancas
        self.taxa = taxa

    def subtotal(self):
        im = self.imovel
        return im.valor_base() + im.valor_quarto_extra() + im.valor_vagas()

    def desconto(self):
        if self.imovel.tem_desconto_sem_criancas() and not self.tem_criancas:
            return round(self.subtotal() * 0.05, 2)
        return 0

    def aluguel_mensal(self):
        return round(self.subtotal() - self.desconto(), 2)

    def mostrar_resumo(self):
        im = self.imovel
        print("")
        print("===== ORCAMENTO RM IMOVEIS =====")
        print("Imovel: " + im.nome())
        print("Aluguel base ........ R$ %.2f" % im.valor_base())
        if im.valor_quarto_extra() > 0:
            print("Quarto extra ........ R$ %.2f" % im.valor_quarto_extra())
        if im.valor_vagas() > 0:
            print("Vagas de garagem .... R$ %.2f" % im.valor_vagas())
        print("Subtotal ............ R$ %.2f" % self.subtotal())
        if self.desconto() > 0:
            print("Desconto 5%% ......... - R$ %.2f" % self.desconto())
        print("ALUGUEL MENSAL ...... R$ %.2f" % self.aluguel_mensal())
        print("")
        print("--- TAXA CONTRATUAL (separada do aluguel) ---")
        print("Valor total ......... R$ %.2f" % TaxaContratual.VALOR)
        if self.taxa.parcelas == 1:
            print("Pagamento ........... a vista")
        else:
            print("Pagamento ........... %dx de R$ %.2f" % (self.taxa.parcelas, self.taxa.valor_parcela()))


# ---------- entrada de dados ----------

def pedir_numero(msg, opcoes):
    while True:
        try:
            n = int(input(msg))
        except ValueError:
            print("Digite um numero.")
            continue
        if n in opcoes:
            return n
        print("Opcao invalida. Escolha entre", opcoes)


def montar_locacao():
    print("Tipo de imovel: 1 - Apartamento  2 - Casa  3 - Estudio")
    tipo = pedir_numero("Escolha: ", [1, 2, 3])

    tem_criancas = False

    if tipo == 3:
        print("Estudio: 0 vagas, ou pacote de 2 vagas (R$ 250) + R$ 60 por vaga extra.")
        vagas = pedir_numero("Quantas vagas? ", list(range(0, 11)))
        while vagas == 1:
            print("No estudio nao existe 1 vaga sozinha. Escolha 0 ou 2 ou mais.")
            vagas = pedir_numero("Quantas vagas? ", list(range(0, 11)))
        imovel = Estudio(vagas)
    else:
        print("Quartos: 1 ou 2")
        quartos = pedir_numero("Escolha: ", [1, 2])
        print("Garagem: 0 = nao, 1 = sim")
        vagas = pedir_numero("Escolha: ", [0, 1])
        if tipo == 1:
            imovel = Apartamento(quartos, vagas)
            resp = input("O cliente tem criancas? (s/n): ").strip().lower()
            tem_criancas = (resp == "s")
        else:
            imovel = Casa(quartos, vagas)

    print("Taxa contratual de R$ 2000,00 pode ser paga em ate 5 parcelas.")
    parcelas = pedir_numero("Em quantas parcelas (1 a 5)? ", [1, 2, 3, 4, 5])

    return Locacao(imovel, tem_criancas, TaxaContratual(parcelas))


# ---------- projecao e csv ----------

def gerar_csv(locacao, nome_arquivo):
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saida")
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    caminho = os.path.join(pasta, nome_arquivo)

    with open(caminho, "w", newline="", encoding="utf-8-sig") as arq:
        escritor = csv.writer(arq, delimiter=";")
        escritor.writerow(["mes", "aluguel_mensal", "taxa_parcela", "total_do_mes"])
        for mes in range(1, 13):
            aluguel = locacao.aluguel_mensal()
            taxa = locacao.taxa.valor_no_mes(mes)
            total = round(aluguel + taxa, 2)
            escritor.writerow([
                mes,
                ("%.2f" % aluguel).replace(".", ","),
                ("%.2f" % taxa).replace(".", ","),
                ("%.2f" % total).replace(".", ","),
            ])
    return caminho


# ---------- programa principal ----------

def main():
    print("=== RentSmart ===")
    locacao = montar_locacao()
    locacao.mostrar_resumo()
    arquivo = gerar_csv(locacao, "projecao_12_meses.csv")
    print("")
    print("Projecao de 12 meses salva em: " + arquivo)


if __name__ == "__main__":
    main()
