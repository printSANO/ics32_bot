import pygsheets
import secretToken

def writeToSheet(cell: str, message: str):
    sheetName = secretToken.sheets
    authorizer = secretToken.sheetsJson

    gc = pygsheets.authorize(service_file=authorizer)
    sh = gc.open(sheetName)
    wk1 = sh.sheet1
    wk1.update_value(cell, message)
    return "Message recorded to spreadsheet"

if __name__ == "__main__":
    writeToSheet("B2","hello")
