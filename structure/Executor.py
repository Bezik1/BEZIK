import pyautogui
import time
import openpyxl
import subprocess
import sys
from os import path, environ, startfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#---------------------------Instructions---------------------------
#   write [program_type]: [program code]
#   open [path] [new_window?]
#   close [program]
#   webdriver [mode] [path] [website_instrucitons?]:
#       form_name [name] [value]
#       submit
#       
#
#

PROGRAM_EXTENSIONS = {
    "python": "py",
    "javascript": "js",
    "typescript": "ts",
    "css": "css",
    "html": "html",
    "java": "java",
    "php": "php",
    "txt": "txt",
    "csv": "csv"
}

WEBDRIVER_SCRIPTS = {
    "highlight": """
    const range = document.createRange();
    const selection = window.getSelection();
    range.selectNodeContents(arguments[0]);
    selection.removeAllRanges();
    selection.addRange(range);
    """,
    "scroll": "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
}

EXCEL_DICT = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']

class Executor():
    def __init__(self) -> None:
        pass

    def text_analize(self, text):
        pass

    def command_list_preparation(self, text):
        return text.split("\n")

    def join_quotes(self, lst):
        result = []
        i = 0
        while i < len(lst):
            if lst[i] == "'":
                # Found the opening quote
                quoted_str = lst[i]
                i += 1
                while i < len(lst) and lst[i] != "'":
                    quoted_str += lst[i]
                    i += 1
                if i < len(lst) and lst[i] == "'":
                    quoted_str += lst[i]
                result.append(quoted_str)
            else:
                result.append(lst[i])
            i += 1
        return result

    def merge_between_parentheses(self, lst):
        result = []
        temp = []
        inside_parentheses = False
        
        for item in lst:
            if item == '[':
                inside_parentheses = True
                temp = []
            elif item == ']':
                inside_parentheses = False
                result.append(''.join(temp))
            elif inside_parentheses:
                temp.append(item)
            else:
                result.append(item)
        
        #print(result)
        return result

    def execute(self, command_list):
        command_type = command_list[0]
        match command_type:
            case 'webdriver':
                command_list = self.join_quotes(command_list)

                mode = command_list[1]
                url = command_list[2]

                driver = webdriver.Edge()
                driver.maximize_window()
                driver.get(url)

                match mode:
                    case "search":
                        page_source = driver.page_source
                        search_text_param = command_list[3][1:-1]

                        try:
                            element = driver.find_element(By.XPATH, f"//*[contains(text(), '{search_text_param}')]")

                            driver.execute_script(WEBDRIVER_SCRIPTS["highlight"], element)
                            driver.execute_script(WEBDRIVER_SCRIPTS["scroll"], element)
                        except:
                            print("Nie odnaleziono tekstu")
                    case _:
                        print("Nieprawidłowy tryb")
                
                time.sleep(7.5)
                driver.quit()
                
            case 'open':
                pyautogui.press('winleft')
                pyautogui.write(command_list[1])
                pyautogui.press('enter')
                time.sleep(2)
            case 'excel':
                # Excel Operations
                #
                # columns
                # formula
                # chart
                #
                
                command_list = self.merge_between_parentheses(command_list)
                wb = openpyxl.Workbook()
                sheet = wb.active

                column_names = command_list[1].split(',')
                column_values = []
                
                for i in range(2, len(command_list)):
                    column_values.append(command_list[i].split(','))
                
                for i, name in enumerate(column_names):
                    sheet[f'{EXCEL_DICT[i]}1'] = name

                for i in range(len(column_names)):
                    for j in range(len(column_values[0])):
                        sheet[f'{EXCEL_DICT[i]}{j+2}'] = column_values[i][j]

                file_path = 'example.xlsx'
                wb.save(file_path)
                startfile(file_path)
            
            case 'write':
                extension = PROGRAM_EXTENSIONS[command_list[1]]
                program = f'''{" ".join(command_list[2:])[1:-1].replace("true", "True").replace("false", "False")}'''[1:]

                # Path
                #desktop_path = path.join(path.join(environ['USERPROFILE']), 'OneDrive\Pulpit')
                #file_path = path.join(desktop_path, f'file.{extension}')
                file_path = f'file.{extension}'

                writer_file = open(file_path, "w")
                writer_file.write(program)
                writer_file.close()

                file = open(file_path, "a")
                subprocess.call(["python", file_path],creationflags=subprocess.CREATE_NEW_CONSOLE)
                
            case _:
                print("Nieprawidłowa komenda")