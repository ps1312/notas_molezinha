from fixtures import one_transaction_pdf, multiple_transactions_pdf
from brokerage_note_parser import process_note_transactions

# Test processing one transaction
def test_process_one_transaction_pdf():
    transactions = process_note_transactions(one_transaction_pdf)
    
    assert len(transactions) == 1
    assert transactions == [{
        'buy_or_sell': 'C',
        'asset_name': 'ACAO',
        'quantity': 5,
        'unit_price': 10.00,
        'total_price': 50.00,
        'taxes': 0.07,
        'total_price_with_taxes': 50.07,
        'average_cost': 10.014,
        'accumulated_quantity': 5,
        'accumulated_aquisition_cost': 50.07
    }]

# Test processing multiple transactions
def test_process_multiple_transactions_pdf():
    transactions = process_note_transactions(multiple_transactions_pdf)

    first_transaction = {
        'buy_or_sell': 'C',
        'asset_name': 'ACAOBALADERA',
        'quantity': 5,
        'unit_price': 10.00,
        'total_price': 50.00,
        'taxes': 1.86,
        'total_price_with_taxes': 51.86,
        'average_cost': 10.372,
        'accumulated_quantity': 5,
        'accumulated_aquisition_cost': 51.86
    }

    second_transaction = {
        'buy_or_sell': 'C',
        'asset_name': 'ACAOTOPZERA',
        'quantity': 2,
        'unit_price': 2.00,
        'total_price': 4.00,
        'taxes': 0.14,
        'total_price_with_taxes': 4.14,
        'average_cost': 2.07,
        'accumulated_quantity': 2,
        'accumulated_aquisition_cost': 4.14
    }

    assert transactions == [first_transaction, second_transaction]