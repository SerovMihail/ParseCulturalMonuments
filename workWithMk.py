# -*- coding: utf-8 -*-

import requests
import json
from urllib.request import urlopen
from urllib.request import urljoin
from lxml.html import fromstring
import supportingFunc as support
import xlwt
import os

def getJsonMK(region):
    """
    Функция отправляет POST запрос на сайт, запрашивая все объекты культурного наследия в регионе "Карелия".
    Ответ получает в виде JSON файла.

    :return dict:
    """

    #тип передаваемого сообщения
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    #тело запроса
    data = "data%5B0%5D%5Bname%5D=CultureObjects%5Bcob_reg_number%5D&data%5B0%5D%5Bvalue%5D=&data%5B1%5D%5Bname%5D=" \
           "CultureObjects%5Bcob_name%5D&data%5B1%5D%5Bvalue%5D=&data%5B2%5D%5Bname%5D=" \
           "CultureObjects%5Bcob_ter_nnn%5D&data%5B2%5D%5Bvalue%5D=" + str(region) + "&data%5B3%5D%5Bname%5D=" \
           "CultureObjects%5Bcob_address%5D&data%5B3%5D%5Bvalue%5D=&data%5B4%5D%5Bname%5D=" \
           "CultureObjects%5Bcob_category_type%5D&data%5B4%5D%5Bvalue%5D=&data%5B5%5D%5Bname%5D=" \
           "CultureObjects%5Bcob_object_type%5D&data%5B5%5D%5Bvalue%5D=&data%5B6%5D%5Bname%5D=" \
           "CultureObjects%5Btypologies%5D&data%5B6%5D%5Bvalue%5D=&data%5B7%5D%5Bname%5D=" \
           "CultureObjects%5Bwdep_osobo%5D&data%5B7%5D%5Bvalue%5D=0&data%5B8%5D%5Bname%5D=" \
           "CultureObjects%5Balb%5D&data%5B8%5D%5Bvalue%5D=0&data%5B9%5D%5Bname%5D=" \
           "CultureObjects%5Bcob_unesco_type%5D&data%5B9%5D%5Bvalue%5D=0&data%5B10%5D%5Bname%5D=" \
           "CultureObjects%5Bcob_status_type%5D&data%5B10%5D%5Bvalue%5D=0"

    urlForGetJson = "https://okn-mk.mkrf.ru/Maps/searchMap"

    request = requests.request('POST', urlForGetJson, data=data, headers=headers) # response 200
    textJson = json.loads(request.text, encoding='utf-8') # представляет в строку, но формат "словарь"
    #print(request.text) # удобочитаемое представление

    return textJson

def fillListMK():
    """
    C помощью данных из JSON используем id для перехода на нужную страницу сайта и извлекаем в словарь
    нужные нам данные.

    :return list of dict:
    """

    # ------------------------- Заполняем из JSON -------------------------------------
    region = 0
    countRussianRegion = 93

    try:
        os.mkdir("mkrfFiles")
    except:
        print('file will be save in "mkrfFiles"')
    os.chdir("mkrfFiles")

    while True:
        try:
            print("Выберите номер региона \t !Ожидается числовой формат от 1 до 92")
            region = int(input())
            if (region > 0 and region < countRussianRegion):
                print("Нужный регион найден")
                break
            else:
                print("Вы выбрали неправильный регион\nСмотри 'СписокРегионовДляМинкульта.txt'")

        except:
            print("Ожидается числовой формат")
            continue

    textJson = getJsonMK(region)

    listOfDictionary = []  # список для хранения массива словарей с id, координаты

    i = 0  # не тру питоновский счётчик
    for features in textJson["features"]: # переписываем данные в удобный словарь
        i = i + 1  # счетчик записей
        mainDictionary = {}  # словарь для заполнения

        # print(features['id']) # проверочка
        # print(features['geometry']) # проверочка №2
        # print(features['geometry']['coordinates'][0]) # проверочка
        # print(features['geometry']['coordinates'][1])
        # print("\n")




        mainDictionary['count'] = i
        mainDictionary['id'] = features['id']
        mainDictionary['coordinate_1'] = features['geometry']['coordinates'][0]
        mainDictionary['coordinate_2'] = features['geometry']['coordinates'][1]

        listOfDictionary.append(mainDictionary)

    #проверка заполнения
    #for i in listOfDictionary:
    #   print("Count: ", i['count'], "| id: ", i['id'], "| coord_1:", i['coordinate_1'], "| cord_2: ",
    #          i['coordinate_2'], '\n')


    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('list')
    # sheet.write(0, 1, "Count")
    # sheet.write(0, 2, "Id")
    # sheet.write(0, 4, "RegNumber")
    # sheet.write(0, 5, "Url")
    # sheet.write(0, 6, "Coordinate_1")
    # sheet.write(0, 7, "Coordinate_2")

    # ------------------------- Заполнение по id через сайт --------------------------------------

    urlForSearch = "https://okn-mk.mkrf.ru/cultureObjects/viewMaps/" # + id объекта

    #Дозаполняем информацию для каждого элемента в списке словарей
    i = 0
    countErrors = 0
    for object in listOfDictionary:
        try:
            #подготовка данных
            urlid = urljoin(urlForSearch, str(object['id'])) # формируем url
            httpResponse = urlopen(urlid) # 200
            list_html = httpResponse.read().decode('utf-8') # Тут уже почемуто кодировка utf-8? непонятный сайт..
            list_doc = fromstring(list_html)

            #извлекаем по css классу
            name = list_doc.cssselect('div.clearfix')[0] # без индекса даже одно единственное совпадение записывается как список
            reg = list_doc.cssselect('.col-sm-12 > div:nth-child(3)')[0]

            """
            adr = list_doc.cssselect('div.col-sm-12 div')


            clearAdr = removeAllUseless(adr.text)
            print(adr.text)
            for i in adr:
                print(i.text)

            """
            clearReg = support.removeAllUseless(reg.text)

            # Потому что кол-во пунктов отличается. И Регистрационный номер может быть на 2 или 3 месте.
            if (clearReg  == "Наименование объекта:"):
               regNumber = list_doc.cssselect('.col-sm-12 > div:nth-child(2)')[0]
            else:
               regNumber = list_doc.cssselect('.col-sm-12 > div:nth-child(3)')[0]

            #if (clearAdr == "")


            object['regNumber'] = support.removeAllUseless(regNumber.text)
            object['url'] = urlid
            object['name'] = support.removeAllUseless(name.text)  # потому что с сайта приходят в непонятном обрамлении
            object['errorParsing'] =False

            # print(object['name'])

        except:
            print("Error in: " + object['url'])
            object['errorParsing'] = True
            countErrors += 1
            continue

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('list')
    sheet.write(0, 0, "Count")
    sheet.write(0, 1, "Id")
    sheet.write(0, 2, "RegNumber")
    sheet.write(0, 3, "Url")
    sheet.write(0, 4, "Coordinate_1")
    sheet.write(0, 5, "Coordinate_2")


    row = 1
    for item in listOfDictionary:
        column = 0

        sheet.write(row, column, item['count'])
        column += 1
        sheet.write(row, column, item['id'])
        column += 1
        sheet.write(row, column, item['regNumber'])
        column += 1
        sheet.write(row, column, item['url'])
        column += 1
        sheet.write(row, column, item['coordinate_1'])
        column += 1
        sheet.write(row, column, item['coordinate_2'])
        column += 1

        row += 1
        workbook.save('reg_' + str(region) + '_mkrf.xls')

    """
    f = open("NewReestr.txt", "w")
    for i in listOfDictionary:
        f.write("\n______________________________________________")
        f.write("%s\n" % i['count'])
        f.write("%s\n" % i['id'])
        f.write("%s\n" % i['regNumber'])
        f.write("%s\n" % i['url'])
        f.write("%s\n" % i['coordinate_1'])
        f.write("%s\n" % i['coordinate_2'])
        f.write("\n______________________________________________")
    f.write("\n====================================================")
    f.write("%s\n" % "Отчет по региону")
    f.write("%s\n" % "Всего объектов культурного наследия в регионе%s" % listOfDictionary['count'])
    f.write("%s\n" % "Ошибок при парсинге%s" % countErrors)


    f.close()



    for i in listOfDictionary:
        print("| Count: ",                   i['count'], '\n',
              "\t| Id: ",                      i['id'], '\n',
              "\t| Registration numbers : ",   i['regNumber'], '\n',
              "\t| Name: ",                    i['name'], '\n',
              "\t| Url: ",                     i['url'], '\n',
              "\t| Coord_1:",                  i['coordinate_1'], '\n',
              "\t| Cord_2: ",                  i['coordinate_2'], '\n',
            "______________________________________________________________" )
    """

    return listOfDictionary