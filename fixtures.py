# Use one_transaction_pdf as reference when creating more fixtures
# transaction format:
# 
# 1-BOVESPA C {VISTA|FRACIONARIO} {NOME_ACAO} {QUANTIDADE} {PRECO_UNIT} {PRECO_TOTAL} D

one_transaction_pdf = """
1-BOVESPA C FRACIONARIO ACAO 5 10,00 50,00 D
Taxa de liquidação 0,05
Valor das operações 50,00
Emolumentos 0,02
"""

multiple_transactions_pdf = """
1-BOVESPA C FRACIONARIO ACAOBALADERA 5 10,00 50,00 D
1-BOVESPA C FRACIONARIO ACAOTOPZERA 2 2,00 4,00 D
Taxa de liquidação 1,00
Valor das operações 54,00
Emolumentos 1,00
"""