import datetime
import pandas as pd
import openpyxl
from recognize import speak


def write_error(error):
    timestamp = datetime.datetime.now()
    df = pd.DataFrame({"Errors": [error], "Time": [timestamp]})

    try:
        existing_data = pd.read_excel("C:\\Users\\aliha\\Documents\\Python Projects\\Voice Assistant\\Errors.xlsx")
        updated_data = pd.concat([existing_data, df], ignore_index=True)
        updated_data.to_excel("C:\\Users\\aliha\\Documents\\Python Projects\\Voice Assistant\\Errors.xlsx", index=False)
        
    except FileNotFoundError:
        df.to_excel("C:\\Users\\aliha\\Documents\\Python Projects\\Voice Assistant\\Errors.xlsx", index=False)


def show_error():
    file_path = "C:\\Users\\aliha\\Documents\\Python Projects\\Voice Assistant\\Errors.xlsx"
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        for row in sheet.iter_rows():
            for cell in row:
                print(cell.value, end="\t")
            print()

        workbook.close()
    except FileNotFoundError:
        speak("File does not exist.")