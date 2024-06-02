import openpyxl

wb = openpyxl.Workbook()

sheet = wb.active

sheet['A1'] = 'id'
sheet['B1'] = 'username'

data = [
    (1, 'mati'),
    (2, 'rudy'),
    (3, 'bezik')
]

for idx, (id_val, username_val) in enumerate(data, start=2):
    sheet[f'A{idx}'] = id_val
    sheet[f'B{idx}'] = username_val

wb.save('example.xlsx')
