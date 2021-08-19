import openpyxl

import constants
import selenium_Funct


# Opening Book as Active so that we can save reports
def function_to_run():
    book = openpyxl.load_workbook("template.xlsx", read_only=False)
    sheet = book.active
    user = constants.username.split("@")[0]
    filename = str(user + " " + constants.list_of_searching_text[0])
    selenium_Funct.selenium_function(sheet, book, filename)



if __name__ == "__main__":
   function_to_run()