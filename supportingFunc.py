import re
import datetime
import xlwt
import xlrd
import time as t
import workWithWiki
import workWithMk
from xlutils.copy import copy
import os

def checkLastUpdate():
    chacheTime = 4 # Изменить дэльту времени тут <====
    firstStart = False

    try:
        rb = xlrd.open_workbook('lastUpdate.xls', formatting_info=True)
        sheet = rb.sheet_by_index(0)
        timeUpdate = sheet.row_values(1)[0]
        timeUpdate = datetime.datetime.fromtimestamp(float(timeUpdate))
        print("Данные обновлялись __ ", timeUpdate, " __ ")
        delta = datetime.timedelta(hours=chacheTime)
        timeUpdate = timeUpdate + delta
    except:
        firstStart = True

    if (firstStart == True):
        print("Файл с данными об обновлениях не найден. Запустить обновление? (Да/Нет)")
    elif (timeUpdate > datetime.datetime.now()):
        print("Данные обновлялись меньше", chacheTime, "-х часов назад\nПродолжить обновление? (Да/Нет)")
    elif (timeUpdate < datetime.datetime.now()):
        print("Данные обновлялись больше", chacheTime, "-х часов назад\nПродолжить обновление? (Да/Нет)")

    while True:
        try:
            accept = str(input())
            if (accept == 'Да'):

                print("Начинается обработка ресурса wikivoyage.org")
                workWithWiki.fillListWiki()


                print("Начинается обработка ресурса mkrf.ru")
                workWithMk.fillListMK()


                print("Сохранение результата")
                setLastUpdate()


                print("Проверка на соответствие памятников архитектуры двух ресурсов")
                compare2files('wikiRegions.xls', 'reg_10_mkrf.xls')

                break
            if (accept == 'Нет'):
                print("Всего доброго, возвращайтесь, когда данные снова устареют")
                break


            else:
                print("Выберите - (Да/Нет)")

        except:
            print("Аварийное завершение работы. Сработало исключение")
            continue

def setLastUpdate():
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('list1')
    sheet.write(0, 0, t.ctime())
    sheet.write(1, 0, t.time())
    workbook.save('lastUpdate.xls')

def compare2files(path1, path2):
    # На чтение первйы файл
    wikiBook = xlrd.open_workbook(path1)

    # На чтение второй файл
    mkrfBook = xlrd.open_workbook(path2)
    mkrfSheet = mkrfBook.sheet_by_index(0)

    # Дополним строки соотвестующие отбору +
    readBook = xlrd.open_workbook(path2, on_demand=True, formatting_info=True)
    read_sheet = readBook.get_sheet(0)  # Читаем из первого листа
    writeBook = copy(readBook)
    write_sheet = writeBook.get_sheet(0)


    mkrfIdColumn = 2
    wikiIdColumn = 3

    for mkrfRows in range(mkrfSheet.nrows):

        mkrfRow = mkrfSheet.row_values(mkrfRows)

        # print(mkrfRows)

        for wikiSheet in range(wikiBook.nsheets):

            currentWikiSheet = wikiBook.sheet_by_index(wikiSheet)

            for wikiRows in range(currentWikiSheet.nrows):


                wikiRow = currentWikiSheet.row_values(wikiRows)



                if (mkrfRow[mkrfIdColumn].replace(' ', '') == wikiRow[wikiIdColumn].replace(' ', '')):
                    # print(mkrfRow) # То что есть в новом реестре, есть и вики


                    write_sheet.write(mkrfRows, 6, "+")

                    writeBook.save(path2)

def removeAllUseless(text):
    """
    Для удаления лишнего из текста
    :param text:
    :return text:
    """

    try:
        result = re.sub("^\s+|\n|\r|\s+$", '', text) # Убирает все отступы, переносы, пробелы
    except:
        result = "="

    return result