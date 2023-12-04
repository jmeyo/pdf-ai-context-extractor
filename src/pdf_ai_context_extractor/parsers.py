"""Custom parsers for specific PDF formats."""
import pandas as pd
import re

def bank_statement_parser(df, filename):
    """Parser for bank statement format."""
    transactions = []

    for idx, row in df.iterrows():
        row_str = ' '.join([str(x) for x in row if pd.notna(x)])

        # Look for dates (DD/MM/YYYY)
        dates = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', row_str)
        # Look for amounts
        amounts = re.findall(r'[+-]?\s*\d+[,\s]\d{2}', row_str)

        if dates and amounts:
            date_op = dates[0]
            amount = amounts[-1].replace(' ', '').replace(',', '.')

            transactions.append({
                'Date': date_op,
                'Description': row_str,
                'Amount': float(amount),
                'Source': filename
            })

    if transactions:
        return pd.DataFrame(transactions)
    return None

PARSERS = {
    'bank_statement': bank_statement_parser,
}
