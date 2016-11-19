# -*- coding: windows-1251 -*-

import requests
import json
from urllib.request import urlopen
from urllib.request import urljoin
from lxml.html import fromstring
import supportingFunc as support

def getJsonMK():
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
           "CultureObjects%5Bcob_ter_nnn%5D&data%5B2%5D%5Bvalue%5D=10&data%5B3%5D%5Bname%5D=" \
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
    textJson = getJsonMK()

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


    # ------------------------- Заполнение по id через сайт --------------------------------------

    urlForSearch = "https://okn-mk.mkrf.ru/cultureObjects/viewMaps/" # + id объекта

    #Дозаполняем информацию для каждого элемента в списке словарей
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

            #print(object)

        except:
            exit(100)





    for i in listOfDictionary:
        print("| Count: ",                   i['count'], '\n',
              "\t| Id: ",                      i['id'], '\n',
              "\t| Registration numbers : ",   i['regNumber'], '\n',
              "\t| Name: ",                    i['name'], '\n',
              "\t| Url: ",                     i['url'], '\n',
              "\t| Coord_1:",                  i['coordinate_1'], '\n',
              "\t| Cord_2: ",                  i['coordinate_2'], '\n',
            "______________________________________________________________" )


    return listOfDictionary