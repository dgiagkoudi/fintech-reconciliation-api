import os
import shutil
import pandas as pd
from src.config import BANK_STATEMENT_PATH, DATE_TOLERANCE_DAYS, ARCHIVE_DIR, DUPLICATES_DIR, INVOICES_DIR, UNMATCHED_DIR

class AdvancedReconciler:
    def __init__(self, invoices_list):
        self.df_invoices = pd.DataFrame(invoices_list)
        self.df_bank = pd.DataFrame()
        
    def load_bank_statement(self):
        try:
            self.df_bank = pd.read_csv(BANK_STATEMENT_PATH)
            self.df_bank['Date'] = pd.to_datetime(self.df_bank['Date'], format='%d/%m/%Y')
            self.df_bank['Amount'] = self.df_bank['Amount'].astype(float)
        except Exception as e:
            print(f"Σφάλμα κατά τη φόρτωση του Bank Statement: {e}")

    def reconcile(self):
        if self.df_invoices.empty:
            print("Δεν βρέθηκαν τιμολόγια για επεξεργασία.")
            return pd.DataFrame()
            
        self.load_bank_statement()
        
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        os.makedirs(DUPLICATES_DIR, exist_ok=True)
        os.makedirs(UNMATCHED_DIR, exist_ok=True)
        
        if self.df_bank.empty:
            print("Δεν υπάρχουν τραπεζικά δεδομένα.")
            self.df_invoices['Status'] = 'Unmatched'
            self.df_invoices['Bank_Match_Date'] = 'N/A'
            return self.df_invoices

        self.df_invoices['Parsed_Date'] = pd.to_datetime(self.df_invoices['date'], format='%d/%m/%Y', errors='coerce')
        
        status_list = []
        match_date_list = []

        for _, invoice in self.df_invoices.iterrows():
            if pd.isna(invoice['Parsed_Date']):
                status_list.append('Unmatched (Invalid Date)')
                match_date_list.append('N/A')
                continue

            matched_transactions = self.df_bank[
                (self.df_bank['Amount'] == float(invoice['amount'])) & 
                (abs((self.df_bank['Date'] - invoice['Parsed_Date']).dt.days) <= DATE_TOLERANCE_DAYS)
            ]

            src_file = os.path.join(INVOICES_DIR, invoice['filename'])

            if not matched_transactions.empty:
                status_list.append('Matched')
                match_date_list.append(matched_transactions.iloc[0]['Date'].strftime('%d/%m/%Y'))
                
                if os.path.exists(src_file):
                    shutil.move(src_file, os.path.join(ARCHIVE_DIR, invoice['filename']))
            else:
                status_list.append('Unmatched')
                match_date_list.append('N/A')
                
                if os.path.exists(src_file):
                    shutil.move(src_file, os.path.join(UNMATCHED_DIR, invoice['filename']))

        self.df_invoices['Status'] = status_list
        self.df_invoices['Bank_Match_Date'] = match_date_list
        
        output_df = self.df_invoices.drop(columns=['Parsed_Date'])
        return output_df