import openpyxl

import constants
import selenium_Funct


# Opening Book as Active so that we can save reports
from graphical_script import guibuild


def function_to_run():
    book = openpyxl.load_workbook("template.xlsx", read_only=False)
    sheet = book.active
    user = constants.username.split("@")[0]
    filename = str(user + " " + list(constants.commaseparated.split(";"))[0])
    selenium_Funct.selenium_function(sheet, book, filename)



if __name__ == '__main__':
    guibuild()