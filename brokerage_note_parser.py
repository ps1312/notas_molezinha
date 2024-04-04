import re
import pdfplumber

transactions_pattern = re.compile(r"\d+-BOVESPA (\w) (VISTA|FRACIONARIO) ((?:FII )?.+?) (\d+) (\d+,\d+) (\d+,\d+)", re.M)
settlement_fee_pattern = re.compile(r'Taxa de liquidação\s+([\d\.,]+)')
emoluments_pattern = re.compile(r'Emolumentos\s+([\d\.,]+)')
total_note_value_pattern = re.compile(r'Valor das operações\s+([\d\.,]+)')

accumulated_quantity = {}
accumulated_aquitision = {}

def extract_taxes(text):
    settlement_fee_match = settlement_fee_pattern.search(text)
    emoluments_match = emoluments_pattern.search(text)

    if settlement_fee_match and emoluments_match:
        return settlement_fee_match.group(1).replace(',', '.'), emoluments_match.group(1).replace(',', '.')

    return 0.00, 0.00

def extract_total_note_value(text):
    match = total_note_value_pattern.search(text)
    if match:
        total_note_value_str = match.group(1)
        total_note_value = float(total_note_value_str.replace('.', '').replace(',', '.'))
        return total_note_value
    return 0

def process_note_transactions(note_text):
    all_transactions = []

    global accumulated_quantity

    settlement_fee_str, emoluments_fee_str = extract_taxes(note_text)
    settlement_fee = float(settlement_fee_str)
    emoluments_fee = float(emoluments_fee_str)
    total_note_price = extract_total_note_value(note_text)
    transactions = transactions_pattern.findall(note_text)

    for transaction in transactions:
        buy_or_sell, _, asset_name, quantity_str, unit_price_str, total_price_str = transaction
        quantity = int(quantity_str)
        unit_price = float(unit_price_str.replace(',', '.'))
        total_price = float(total_price_str.replace(',', '.'))
        proportion = round(total_price / total_note_price, 2)
        taxes = (proportion * settlement_fee) + (proportion * emoluments_fee)

        total_price_with_taxes = None
        new_quantity = None

        if buy_or_sell == "C":
            total_price_with_taxes = total_price + taxes
            accumulated_aquitision[asset_name] = accumulated_aquitision.get(asset_name, 0) + total_price_with_taxes
            new_quantity = accumulated_quantity.get(asset_name, 0) + quantity
        else:
            total_price_with_taxes = total_price - taxes
            accumulated_aquitision[asset_name] = accumulated_aquitision.get(asset_name, 0) - total_price_with_taxes
            new_quantity = accumulated_quantity.get(asset_name, 0) - quantity

        average_cost = total_price_with_taxes / quantity
        accumulated_quantity[asset_name] = new_quantity

        model = {
            "buy_or_sell": buy_or_sell,
            "asset_name": asset_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": total_price,
            "taxes": round(taxes, 3),
            "total_price_with_taxes": round(total_price_with_taxes, 2),
            "average_cost": average_cost,
            "accumulated_quantity": accumulated_quantity[asset_name],
            "accumulated_aquisition_cost": accumulated_aquitision[asset_name]
        }

        all_transactions.append(model)
    
    return all_transactions

def extract_and_process_notes(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        note_texts = []

        for page in pdf.pages:
            text = page.extract_text()
            note_texts.append(text)

            if "CONTINUA" not in text:
                note_text = "\n".join(note_texts)
                process_note_transactions(note_text)
                note_texts = []

        if note_texts:
            note_text = "\n".join(note_texts)
            process_note_transactions(note_text)