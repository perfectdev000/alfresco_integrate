#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from __future__ import print_function
import pickle
import os.path
# import gspread
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# from oauth2client.service_account import ServiceAccountCredentials

# import xlrd
# from openpyxl import load_workbook

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.

def create_sheet(title):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    # title = "test_sheet"
    spreadsheet = {
        'properties': {
        'title': title
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet,   fields='spreadsheetId').execute()
    # print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
    return spreadsheet.get('spreadsheetId')

def push_sheet(local_name, spreadsheet_id):
    try:
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        if local_name[-4:]=='xlsx':
            workbook = load_workbook(local_name)
            all_sheets = workbook.get_sheet_names()
            first_sheet = all_sheets[0]
            worksheet = workbook.get_sheet_by_name(first_sheet)
            values=[]
            row_cou=worksheet.max_row
            col_cou=worksheet.max_column
            for row in worksheet.iter_rows():
                row_val=[]
                for cell in row:
                    row_val.append(cell.value)
                values.append(row_val)
            # get cell with row number and column number
            # worksheet.cell(row=1, column=2).value
            str_char='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            str_col=''
            for i in range(int(col_cou/26)-1):
                str_col+='A'
            str_col+=str_char[(col_cou % 26)-1:col_cou % 26]

            rangeName = "Sheet1!A1:{}{}".format(str_col,str(row_cou))
            print(rangeName, values)
            Body = {
                'values' : values,
                # 'majorDimension' : 'COLUMNS',
            }
            result = service.spreadsheets().values().update(   spreadsheetId=spreadsheet_id, range=rangeName,    valueInputOption='RAW', body=Body).execute()
            # print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
        else :
            wb = xlrd.open_workbook(local_name)
            sheet = wb.sheet_by_index(0)
            values=[]
            row_cou=sheet.nrows
            col_cou=sheet.ncols
            for i in range(row_cou):
                row_val=[]
                for j in range(col_cou):
                    row_val.append(sheet.cell_value(i,j))
                values.append(row_val)

            str_char='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            str_col=''
            for i in range(int(col_cou/26)-1):
                str_col+='A'
            str_col+=str_char[(col_cou % 26)-1:col_cou % 26]

            rangeName = "Sheet1!A1:{}{}".format(str_col,str(row_cou))
            print(rangeName, values)
            Body = {
                'values' : values,
                # 'majorDimension' : 'COLUMNS',
            }
            result = service.spreadsheets().values().update(   spreadsheetId=spreadsheet_id, range=rangeName,    valueInputOption='RAW', body=Body).execute()

        return True
    except Exception as e:
        print("update google sheet error: ", str(e))
        return False


