import re
import datetime
import xlwt
import xlrd
import time as t
import workWithWiki
import workWithMk
from xlutils.copy import copy


def removeAllUseless(text):
    """
    Для удаления лишнего из текста
    :param text:
    :return text:
    """

    try:
        result = re.sub("^\s+|\n|\r|\s+$", '', text) # Убирает все отступы, переносы, пробелы
    except:
        result = "12 = 12"

    return result


def checkLastUpdate():
    chacheTime = 4

    try:
        rb = xlrd.open_workbook('lastUpdate.xls', formatting_info=True)
    except:
        setLastUpdate()
        rb = xlrd.open_workbook('lastUpdate.xls', formatting_info=True)

    sheet = rb.sheet_by_index(0)
    timeUpdate =  sheet.row_values(1)[0]
    timeUpdate = datetime.datetime.fromtimestamp(float(timeUpdate))
    print("Данные обновлялись __ ", timeUpdate, " __ ")
    actualDate = datetime.timedelta(hours=chacheTime)
    timeUpdate = timeUpdate - actualDate

    if ( datetime.datetime.now() > timeUpdate ):

        while True:
            try:
                print("Данные обновлялись меньше", chacheTime,"-х часов назад\nПродолжить обновление? (Да/Нет)")
                accept = str(input())
                if (accept == 'Да'):

                    workWithWiki.fillListWiki()



                    workWithMk.fillListMK()

                    setLastUpdate()

                    break
                if (accept == 'Нет'):
                    print("Всего доброго, возвращайтесь, когда данные снова устареют")
                    break


                else:
                    print("Выберите - (Да/Нет)")

            except:
                print("Ожидается вменяемый ответ ;)")
                continue
    else:
        print(timeUpdate)




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


    # read_book = xlrd.open_workbook(source_filename, on_demand=True)  # Открываем исходный документ
    # read_sheet = read_book.get_sheet(0)  # Читаем из первого листа
    # write_book = xlcopy(read_book)  # Копируем таблицу в память, в неё мы ниже будем записывать
    # write_sheet = write_book.get_sheet(0)  # Будем записывать в первый лист
    # write_sheet.write(0, 0, read_sheet.cell_value(0, 0) + 42)  # Прибавим к значению из ячейки "A1" число 42
    # write_book.save(destination_filename)



    # print(wikiSheet.cell(1, 0).value)
    # print(mkrfSheet.cell(1, 0).value)

    mkrfIdColumn = 2
    wikiIdColumn = 3

    # style = xlwt.XFStyle()

    # pattern = xlwt.Pattern()
    # pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    # pattern.pattern_fore_colour = xlwt.Style.colour_map['red']
    # style.pattern = pattern
    # sheet.write(0, 0, "Some data", style)

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
