import os
import csv
from fpdf import FPDF

def create_folders():
    os.makedirs('data/invoices', exist_ok=True)
    print("Δημιουργήθηκαν οι φάκελοι data/invoices/")

def generate_mock_bank_statement():
    path = 'data/bank_statements.csv'
    headers = ['Date', 'Description', 'Amount']
    rows = [
        ['24/06/2026', 'INTEREST PAYMENT', '2.10'],
        ['25/06/2026', 'CUSTOMER INBOUND 992', '150.50'],
        ['26/06/2026', 'REMITTANCE ACME CORP', '450.00'],
        ['27/06/2026', 'ERRONEOUS TRANSFER', '12.00']
    ]
    
    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print("Δημιουργήθηκε το αρχείο: data/bank_statements.csv")

def generate_mock_pdf_invoice():
    path = 'data/invoices/invoice_1024.pdf'
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    pdf.cell(200, 10, text="INVOICE / TIMOLOGIO PAROHIS YPIRESION", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    pdf.cell(200, 10, text="Company: ACME CORP", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text="ΑΦΜ : 123456789", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text="Date : 26/06/2026", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.cell(200, 10, text="Description: Web Development & Marketing Services", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text="Net Amount: 362.90 EUR", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text="VAT (24%): 87.10 EUR", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(200, 10, text="Total : 450,00", new_x="LMARGIN", new_y="NEXT")
    
    pdf.output(path)
    print("Δημιουργήθηκε το PDF: data/invoices/invoice_1024.pdf")

if __name__ == "__main__":
    print("=== Dimiourgia Deigmaton Dedomenon ===")
    create_folders()
    generate_mock_bank_statement()
    generate_mock_pdf_invoice()
    print("=== Etoimo! Tora mporeis na trexeis to main.py ===")