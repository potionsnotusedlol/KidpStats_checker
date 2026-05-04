from openpyxl import load_workbook

def parseUsers(fileName: str):
    user_file = load_workbook(fileName).active

    for row in user_file.iter_rows(min_row=2, max_col=2, max_row=4, values_only=True): # type: ignore
        print(row)

def StudentDataHandler():
    # parseUsers()