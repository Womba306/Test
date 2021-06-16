
# импрорт
import PySimpleGUI as sg
import pyodbc
from datetime import datetime

#настройки
connection = pyodbc.connect(("Driver={ODBC Driver 17 for SQL Server};Server=MGP5-SPG04;Database=Test1;Trusted_Connection=yes;UID=sa;PWD=111qqqAAA"))
dbCursor = connection.cursor()
sg.theme('dark grey 9')
now = datetime.now()
Datatime = datetime.now()
print(datetime.now())

#получение списка товаров
def UpdateList():
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
    return new_list

#интерфейс
layout = [
    [sg.Text('Введите товар'),sg.Listbox(UpdateList(), size=(8,15), key='-KTovar1-'),sg.InputText(size=(50,6),key='-KTovar2-')],
    [sg.Text('Количество товара'),sg.InputText(size=(8,3),key='-KCountTovar-')],
    [sg.Output(size=(88, 20),key="-KInputText-")],
    [sg.Submit("Сохранить"), sg.Cancel("Обновить")]
]
window = sg.Window('Поставки', layout)

event, values = window.read()
while event not in (None,"Exit"):
    event, values = window.read()
    if event == "Сохранить":
        sql = 'EXEC [dbo].[BazaMSKInsert] @Tovar=?,@Count=?,@Data=?'
        params = (values['-KTovar2-'], values['-KCountTovar-'], Datatime)
        dbCursor.execute(sql, params)
        dbCursor.commit()
        print(params)
    if event == "Обновить":
        values['-KTovar1-']=UpdateList()
    window.refresh()





