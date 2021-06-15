import PySimpleGUI as sg
import pyodbc
from datetime import datetime
# импрорт

connection = pyodbc.connect(("Driver={ODBC Driver 17 for SQL Server};Server=MGP5-SPG04;Database=Test1;Trusted_Connection=yes;UID=sa;PWD=111qqqAAA"))
dbCursor = connection.cursor()
sg.theme('dark grey 9')

#настройки
dbCursor.execute("select Tovar from BazaMSK")
data = dbCursor.fetchall()

new_list = ['']
for word in data:
    new_str = ''
    for w in word:
        if w.isalpha():
            new_str += w
    new_list.append(new_str)
new_str = ','.join(w for w in new_list if w)
layout = [
    [sg.Text('Выберите товар или введите новый'),sg.Listbox(new_list, size=(8,len(data)), key='-KTovar1-'),sg.InputText(size=(50,6),key='-KTovar2-')],
    [sg.Text('Количество товара'),sg.InputText(size=(8,3),key='-KCountTovar-')],
    [sg.Output(size=(88, 20))],
    [sg.Submit("Сохранить"), sg.Cancel("Закрыть")]
]
window = sg.Window('Поставки', layout)
while True:
    event, values = window.read()
    if event in (None, 'Exit', 'Закрыть'):
        print(event, values)
        break
    if event == "Сохранить" :
        if values['-KTovar1-']== None:
            print(*values['-KTovar1-'], *values['-KCountTovar-'])
        if values['-KTovar2-'] != None:
            print(*values['-KTovar2-'], *values['-KCountTovar-'])

#интерфейс