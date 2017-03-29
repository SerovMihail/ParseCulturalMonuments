import re
import datetime
import xlwt
import xlrd
import time as t
import workWithWiki
import workWithMk


def removeAllUseless(text):
    """
    Для удаления лишнего из текста
    :param text:
    :return text:
    """
    result = re.sub("^\s+|\n|\r|\s+$", '', text) # Убирает все отступы, переносы, пробелы

    return result


def checkLastUpdate():
    chacheTime = 4

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

                    # workWithWiki.fillListWiki()



                    # workWithMk.fillListMK()

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
