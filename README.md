# FinTech Reconciliation Enterprise API

An automated FinTech microservice designed to handle invoice processing and real-time bank statement cross-referencing (reconciliation). The system ingests PDF invoices, extracts structured financial data using smart text processing, validates records against financial logs, syncs clean outputs to the cloud, and dispatches automated accounting alerts.

## Features

- Automated Data Ingestion: FastAPI web endpoints supporting file multi-part uploads.
- Smart PDF Parsing: Robust Regex-based text processing engineered to extract Greek metadata (AFM, Totals, Dates) with parenthesis and formatting resilience.
- Core Reconciliation Engine: Data structures managed with Pandas to perform algorithmic transaction cross-referencing within custom date tolerance windows ($DATE\_TOLERANCE\_DAYS$).
- Storage Optimization Pipeline: Automated file routing into structured directories (`archive`, `duplicates`, `unmatched`) keeping ingestion buckets clean.
- Cloud Integration: Live synchronization with Google Sheets API v4 using safe string mutation to prevent dataset schema mismatch.
- Asynchronous Email Alerts: Immediate accounting notification dispatches for `unmatched` items using `aiosmtplib`.

## Tech Stack

Core
- Python
- FastAPI
- Uvicorn

Data Processing & APIs
- Pandas
- Google Sheets API v4
- Google Auth / Service Accounts

Automation & Delivery
- aiosmtplib (Async SMTP)
- Pypdf / pdfplumber (PDF Text Extraction)
- Python-Dotenv

## Project Structure
```text
FinTech Automation/
├── data/
│   ├── archive/              # Successfully matched historical PDFs
│   ├── duplicates/           # Duplicate invoice logs
│   ├── invoices/             # Ingestion pool for new PDF invoices
│   ├── unmatched/            # PDFs flagged for manual review
│   └── bank_statements.csv   # Local ledger export from bank stream
│
├── src/
│   ├── config.py             # App environment configuration loader
│   ├── email_service.py      # Async SMTP notification generator
│   ├── pdf_parser.py         # Text mining & invoice metadata extraction
│   ├── reconciler.py         # Main Pandas transaction matching engine
│   └── sheets_service.py     # Google Sheets transaction data loader
│
├── credentials.json          # Google Cloud Service Account key (ignored)
├── generate_mock_data.py     # Local sandbox populator script
└── main.py                   # Central API Router & Service Entrypoint
```

## Local Setup

1. Clone repository

```bash
git clone https://github.com/dgiagkoudi/fintech-reconciliation-api.git
cd fintech-reconciliation-api
```

2. Create `.env` file

```env
SHEET_NAME=Sheet1
SMTP_USER="username"
SMTP_PASSWORD="password"
SPREADSHEET_ID="google_sheet_id"
```

3. Google Sheets Setup
   - Create a Google Cloud Platform Service Account.
   - Generate and download the private key as `credentials.json`.
   - Place `credentials.json` directly into the root directory.
   - Open your Google Sheet browser tab, share the sheet with the Service Account email address, and grant Editor permissions.

## Run Project

Populate Sandbox Environments (Optional): Generates mock bank statements and structures local directories:
```bash
python generate_mock_data.py
```

Run Application Server: Fire up the local development web server
```bash
uvicorn main:app --reload
```

## Usage

1. Open your browser and navigate to the interactive Swagger docs: `http://127.0.0.1:8000/docs`.
2. Use the Ingestion Pool (`POST /api/v1/upload-invoice/`) to upload PDF invoices into the application loop.
3. Execute the Core Engine (`POST /api/v1/trigger-reconciliation/`) to process data matching.

## License

This project is licensed under the MIT License.
