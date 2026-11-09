# RentSmart - Orcamento de Locacao (R.M Imoveis)

Trabalho de Algoritmos e Introducao a POO em Python.

## Como executar

Precisa so do Python 3 (sem bibliotecas extras).

```bash
python main.py
```

O programa pergunta o tipo de imovel, quartos, garagem, criancas (so para apartamento) e o numero de parcelas da taxa contratual. Mostra o orcamento e grava `saida/projecao_12_meses.csv`.

## Testes

```bash
python -m unittest test_rentsmart -v
```

## Premissas assumidas (o enunciado nao diz)

- Casa e apartamento: no maximo 1 vaga de garagem.
- Estudio: 0 vagas ou 2 ou mais (1 vaga sozinha nao tem preco).
- Desconto de 5% (apartamento sem criancas) incide sobre base + quarto extra + garagem.
- Taxa contratual de R$ 2.000 sem juros, parcelas com centavos ajustados na ultima.
- Projecao: aluguel constante nos 12 meses; parcelas da taxa a partir do mes 1.

## Estrutura

- `main.py`: classes `Imovel`, `Apartamento`, `Casa`, `Estudio`, `TaxaContratual`, `Locacao` e funcoes de entrada/CSV.
- `test_rentsmart.py`: testes unitarios dos calculos.
- `saida/`: CSV gerado (separador `;` e virgula decimal, para abrir no Excel).
