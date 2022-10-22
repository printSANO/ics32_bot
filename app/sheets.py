import pygsheets
import secretToken

sheetName = secretToken.sheets
authorizer = secretToken.sheetsJson
startNum = 1

def writeToSheet(content: list):
    """Update spreadsheet"""
    global startNum
    gc = pygsheets.authorize(service_file=authorizer)
    sh = gc.open(sheetName)
    wk1 = sh.sheet1
    for i in range(startNum,1000):
        cell = f"A{i}"
        if wk1.get_value(cell) == "":
            wk1.append_table(content,start=cell)
            startNum = i
            break
    return (startNum,"Message recorded to spreadsheet")

if __name__ == "__main__":
    writeToSheet(["B2","hello"])
