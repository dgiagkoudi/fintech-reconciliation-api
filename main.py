import os
import shutil
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from src.pdf_parser import InvoiceParser
from src.reconciler import AdvancedReconciler
from src.sheets_service import GoogleSheetsService
from src.config import INVOICES_DIR

app = FastAPI(title="FinTech Reconciliation Enterprise API")

class ReconciliationSummary(BaseModel):
    total_processed: int
    matched_count: int
    unmatched_count: int
    status: str

@app.post("/api/v1/upload-invoice/", tags=["Ingestion Pool"])
async def upload_invoice(file: UploadFile = File(...)):
    os.makedirs(INVOICES_DIR, exist_ok=True)
    file_path = os.path.join(INVOICES_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "status": "Successfully Uploaded"}

@app.post("/api/v1/trigger-reconciliation/", response_model=ReconciliationSummary, tags=["Core Engine"])
async def trigger_reconciliation():
    # 1. Parsing των PDF τιμολογίων
    parser = InvoiceParser()
    raw_invoices = parser.parse_all_invoices()
    
    if not raw_invoices:
        return ReconciliationSummary(
            total_processed=0, 
            matched_count=0, 
            unmatched_count=0, 
            status="No active invoices found in input directory"
        )
        
    reconciler = AdvancedReconciler(raw_invoices)
    df_result = reconciler.reconcile()
    
    matched = int((df_result['Status'] == 'Matched').sum())
    unmatched = int((df_result['Status'] == 'Unmatched').sum())
    
    try:
        sheets_service = GoogleSheetsService()
        sheets_service.upload_dataframe(df_result)
        sync_status = "Pipeline Executed & Google Sheet Updated Successfully"
    except Exception as e:
        sync_status = f"Reconciliation complete, but Google Sheet failed: {str(e)}"
    
    return ReconciliationSummary(
        total_processed=len(df_result),
        matched_count=matched,
        unmatched_count=unmatched,
        status=sync_status
    )