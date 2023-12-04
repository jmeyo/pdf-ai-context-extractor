#!/usr/bin/env python3
"""
Generate anonymized sample PDFs for testing.

Creates realistic but anonymized sample documents that can be safely
shared in the GitHub repository.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from pathlib import Path
import random
from datetime import datetime, timedelta


def generate_bank_statement_pdf(output_path: Path):
    """Generate a sample bank statement PDF."""

    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("<b>BANK STATEMENT - Sample Account</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))

    # Account info
    info_data = [
        ['Account Holder:', 'John DOE'],
        ['Account Number:', '****1234'],
        ['Period:', 'January 2024'],
        ['Balance:', '$2,345.67'],
    ]
    info_table = Table(info_data, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))

    # Transactions table
    transactions_data = [
        ['Date', 'Description', 'Amount', 'Balance']
    ]

    # Generate sample transactions
    start_date = datetime(2024, 1, 1)
    balance = 2500.0

    sample_transactions = [
        ('Salary Deposit', 3000.00),
        ('Supermarket Purchase', -85.50),
        ('Utility Bill - Electricity', -120.00),
        ('Online Purchase', -45.99),
        ('ATM Withdrawal', -200.00),
        ('Restaurant', -67.80),
        ('Gas Station', -55.30),
        ('Insurance Premium', -95.00),
        ('Pharmacy', -28.45),
        ('Transfer to Savings', -500.00),
    ]

    for i, (desc, amount) in enumerate(sample_transactions):
        date = (start_date + timedelta(days=i*3)).strftime('%d/%m/%Y')
        balance += amount
        transactions_data.append([
            date,
            desc,
            f"${amount:.2f}",
            f"${balance:.2f}"
        ])

    trans_table = Table(transactions_data, colWidths=[1.2*inch, 3*inch, 1.2*inch, 1.2*inch])
    trans_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    elements.append(trans_table)

    # Build PDF
    doc.build(elements)
    print(f"✓ Generated: {output_path.name}")


def generate_invoice_pdf(output_path: Path):
    """Generate a sample invoice PDF."""

    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("<b>INVOICE</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))

    # Invoice info
    info_data = [
        ['Invoice #:', 'INV-2024-001'],
        ['Date:', '15/01/2024'],
        ['Customer:', 'ABC Corporation'],
        ['Payment Terms:', 'Net 30'],
    ]
    info_table = Table(info_data, colWidths=[1.5*inch, 3*inch])
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))

    # Line items
    items_data = [
        ['Item', 'Description', 'Qty', 'Price', 'Total']
    ]

    sample_items = [
        ('Consulting Services', 'Technical consulting - January', 20, 150.00),
        ('Software License', 'Annual subscription', 1, 500.00),
        ('Training Session', '2-day workshop', 2, 800.00),
    ]

    for item, desc, qty, price in sample_items:
        total = qty * price
        items_data.append([
            item,
            desc,
            str(qty),
            f"${price:.2f}",
            f"${total:.2f}"
        ])

    # Add totals
    subtotal = sum(qty * price for _, _, qty, price in sample_items)
    tax = subtotal * 0.10
    total = subtotal + tax

    items_data.extend([
        ['', '', '', 'Subtotal:', f"${subtotal:.2f}"],
        ['', '', '', 'Tax (10%):', f"${tax:.2f}"],
        ['', '', '', 'Total:', f"${total:.2f}"],
    ])

    items_table = Table(items_data, colWidths=[1.5*inch, 2.5*inch, 0.7*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -4), 0.5, colors.black),
        ('LINEABOVE', (3, -3), (-1, -3), 1, colors.black),
        ('LINEABOVE', (3, -1), (-1, -1), 2, colors.black),
    ]))
    elements.append(items_table)

    doc.build(elements)
    print(f"✓ Generated: {output_path.name}")


def generate_simple_table_pdf(output_path: Path):
    """Generate a simple data table PDF."""

    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("<b>SAMPLE DATA TABLE</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))

    # Simple table
    data = [
        ['ID', 'Name', 'Category', 'Value'],
        ['001', 'Item A', 'Type 1', '150.00'],
        ['002', 'Item B', 'Type 2', '275.50'],
        ['003', 'Item C', 'Type 1', '99.99'],
        ['004', 'Item D', 'Type 3', '450.00'],
        ['005', 'Item E', 'Type 2', '125.00'],
    ]

    table = Table(data, colWidths=[0.8*inch, 2*inch, 1.5*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
    ]))
    elements.append(table)

    doc.build(elements)
    print(f"✓ Generated: {output_path.name}")


def main():
    """Generate all sample PDFs."""

    # Check if reportlab is installed
    try:
        import reportlab
    except ImportError:
        print("❌ reportlab not installed")
        print("   Install with: pip install reportlab")
        return

    samples_dir = Path(__file__).parent / "samples"
    samples_dir.mkdir(exist_ok=True)

    print("\n" + "="*80)
    print("GENERATING ANONYMIZED SAMPLE PDFs")
    print("="*80)
    print()

    # Generate samples
    generate_bank_statement_pdf(samples_dir / "sample_bank_statement.pdf")
    generate_invoice_pdf(samples_dir / "sample_invoice.pdf")
    generate_simple_table_pdf(samples_dir / "sample_data_table.pdf")

    print()
    print("="*80)
    print(f"✅ Generated 3 sample PDFs in: {samples_dir}")
    print("="*80)
    print()
    print("These anonymized PDFs can be safely committed to the repository")
    print("for testing and demonstration purposes.")
    print()


if __name__ == "__main__":
    main()
