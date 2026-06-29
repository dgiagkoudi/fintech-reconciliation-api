import os
import re
from pypdf import PdfReader
from src.config import INVOICES_DIR

class InvoiceParser:
    def __init__(self):
        self.afm_pattern = re.compile(r'(?:ΑΦΜ|Α\.Φ\.Μ\.|AFM)\s*[:\-.\s]?\s*(\d{9})', re.IGNORECASE)
        
        self.amount_pattern = re.compile(r'(?:Σύνολο|Πληρωτέο|Total)(?:\s*\([^)]+\))?\s*[:\-.\s]?\s*([\d.,]+)', re.IGNORECASE)
        
        self.date_pattern = re.compile(r'(\d{2}[-/]\d{2}[-/]\d{4})')

    def extract_text_from_pdf(self, pdf_path):
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"Σφάλμα κατά την ανάγνωση του {pdf_path}: {e}")
            return ""

    def parse_invoice(self, filename):
        pdf_path = os.path.join(INVOICES_DIR, filename)
        text = self.extract_text_from_pdf(pdf_path)
        
        afm_match = self.afm_pattern.search(text)
        amount_match = self.amount_pattern.search(text)
        date_match = self.date_pattern.search(text)
        
        afm = afm_match.group(1) if afm_match else "Unknown"
        
        amount = 0.0
        if amount_match:
            raw_amount = amount_match.group(1).replace('.', '').replace(',', '.')
            try:
                amount = float(raw_amount)
            except ValueError:
                amount = 0.0

        date = date_match.group(1) if date_match else "Unknown"
        
        return {
            "filename": filename,
            "afm": afm,
            "amount": amount,
            "date": date
        }

    def parse_all_invoices(self):
        invoices_data = []
        if not os.path.exists(INVOICES_DIR):
            os.makedirs(INVOICES_DIR)
            return invoices_data
            
        for file in os.listdir(INVOICES_DIR):
            if file.endswith('.pdf'):
                data = self.parse_invoice(file)
                invoices_data.append(data)
        return invoices_data