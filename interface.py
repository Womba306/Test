
# импрорт
import re
from datetime import datetime

import PySimpleGUI as sg
import pyodbc

#настройки
connection = pyodbc.connect(("Driver={ODBC Driver 17 for SQL Server};Server=MGP5-SPG04;Database=Test1;Trusted_Connection=yes;UID=sa;PWD=111qqqAAA"))
dbCursor = connection.cursor()
sg.theme('dark grey 9')
now = datetime.now()
Datatime = datetime.now()
print(datetime.now())


#Проверка на спец символ
def detect_special_characer(pass_string):
  regex= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
  if(regex.search(pass_string) == None):
    res = False
  else:
    res = True
  return(res)
#получение списка товаров

def UpdateList(sql):
    dbCursor.execute(sql)
    data = dbCursor.fetchall()
    new_list = []
    for word in data:
        new_str = ''
        for w in word:
            if detect_special_characer(w)==False:
                new_str += w
        new_list.append(new_str)
    new_str = ','.join(w for w in new_list if w)
    for i in range(len(new_list)):
        new_list[i]=new_list[i].lower()
    return new_list


#интерфейс
#layout1 = [sg.Table("1")]
#window1 = sg.Window('Таблица поставок', layout1)
#event1, values1 = window1.read()
layout = [
    [sg.Text('Введите товар'),sg.Combo(UpdateList('Select Tovar from BazaMSK'), size=(30,15), key='-KTovar1-'),sg.Text('Введите производителя'),sg.Combo(UpdateList('EXEC [dbo].[Proiz_Select]'), size=(30,15), key='-KProiz-')],
    [sg.Text('Количество товара'),sg.InputText(size=(8,3),key='-KCountTovar-')],
    [sg.Output(size=(88, 20),key="-KInputText-")],
    [sg.Submit("Сохранить"), sg.Submit("Обновить")]
]
window = sg.Window('Поставки', layout)
event, values = window.read()
while event not in (None,"Exit"):
    event, values = window.read()
    if values['-KProiz-'] != '':
        sql = 'EXEC [dbo].[BazaMskFindProiz] @Tovar=?'
        params = values['-KProiz-']
        dbCursor.execute(sql, params)
        dbCursor.commit()

    if event == "Сохранить":
        sql = 'EXEC [dbo].[BazaMSKInsert] @Tovar=?,@Count=?,@Data=?,@IdProiz=?'
        params = (values['-KTovar1-'], values['-KCountTovar-'], Datatime, (values['-KProiz-'].split())[1])
        dbCursor.execute(sql, params)
        dbCursor.commit()
        print("Добвленно",values['-KCountTovar-'], values['-KTovar1-'],"в",(values['-KProiz-'].split())[0])
    if event == "Обновить":
        window['-KTovar1-'].update(values=UpdateList('Select Tovar from BazaMSK'))
        window['-KProiz-'].update(values=UpdateList('EXEC [dbo].[Proiz_Select]'))
        print("Обновляем данные,", datetime.now())
        print(UpdateList('EXEC [dbo].[BazaMSK_Select]'))
        #window1[layout1].update()






