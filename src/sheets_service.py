from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from src.config import CREDENTIALS_PATH, SPREADSHEET_ID, RANGE_NAME

class GoogleSheetsService:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.credentials = Credentials.from_service_account_file(
            CREDENTIALS_PATH, scopes=self.scopes
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)

    def upload_dataframe(self, dataframe):
        if dataframe.empty:
            print("Το DataFrame είναι άδειο. Δεν ανέβηκε τίποτα.")
            return
            
        try:
            df_clean = dataframe.astype(str).fillna("")
            
            header = df_clean.columns.tolist()
            rows = df_clean.values.tolist()
            values = [header] + rows

            body = {
                'values': values
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            print("--- Google Sheets Sync Complete ---")
            print(f"Ενημερώθηκαν επιτυχώς {result.get('updatedCells')} κελιά στο αρχείο σου!")
            
        except Exception as e:
            print(f"Κρίσιμο Σφάλμα κατά την επικοινωνία με το Google Sheets API: {e}")
            raise e