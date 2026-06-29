import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, 'data')
INVOICES_DIR = os.path.join(DATA_DIR, 'invoices')
ARCHIVE_DIR = os.path.join(DATA_DIR, 'archive')
DUPLICATES_DIR = os.path.join(DATA_DIR, 'duplicates')
UNMATCHED_DIR = os.path.join(DATA_DIR, 'unmatched')

BANK_STATEMENT_PATH = os.path.join(DATA_DIR, 'bank_statements.csv')
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID') 
RANGE_NAME = 'Sheet1!A1'

DATE_TOLERANCE_DAYS = 3

SMTP_HOST = "smtp.mailtrap.io"
SMTP_PORT = 2525
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_FROM = "reconciler@fintech.internal"
EMAIL_TO = "accounting@company.com"