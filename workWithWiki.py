# -*- coding: utf-8-*-

import wptools #  Api Wiki
import re
import supportingFunc as support
from urllib.request import urlopen
from urllib.request import urljoin
from lxml.html import fromstring
import requests
import os
import xlwt


def getNameAndHref():
    pass

def parseAlmostSameBlock(list_doc, lowblock, hightblock):
    """
    возможно со строки 51 стоит преобрзовать цикл в фукнцию?
    :param list_doc:
    :param lowblock:
    :param hightblock:
    :return:
    """

    pass



def getKareliaDistrictsWiki():

    urlSite = "https://ru.wikivoyage.org/"

    kareliaListPages = []

    url = "https://ru.wikivoyage.org/wiki/%D0%9A%D1%83%D0%BB%D1%8C%D1%82%D1%83%D1%80%D0%BD%D0%BE%D0%B5" \
          "_%D0%BD%D0%B0%D1%81%D0%BB%D0%B5%D0%B4%D0%B8%D0%B5_" \
          "%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8/%D0%9A%D0%B0%D1%80%D0%B5%D0%BB%D0%B8%D1%8F"

    httpResponse = urlopen(url)
    list_html = httpResponse.read().decode('utf-8')
    list_doc = fromstring(list_html)


    """
    Изначально selectLowBlock = False - обрабатываем верхний блок
    После этого selectLowBlock = True, обнулили счётчики и переключились на нижнй блок
    """
    selectLowBlock = False
    count = 1 # счётчик записей для удобства записи
    i=0 # для прохода по данным

    while True: # ������������ do-while
        try:
            if (selectLowBlock == False):
                select = list_doc.cssselect('#mw-customcollapsible-myDiv2 > div:nth-child(1) '
                                            '> p:nth-child(2) > small:nth-child(1) > a')[i]
            if (selectLowBlock == True):
                select = list_doc.cssselect('#mw-customcollapsible-myDiv2 > div:nth-child(1) '
                                            '> p:nth-child(3) > small:nth-child(1) > a')[i]

            dic = {}
            dic['count'] = count
            secondPartUrl = select.get('href')
            dic['href'] = urljoin(urlSite, secondPartUrl)
            dic['name'] = select.text


            i = i + 1
            count = count + 1

            kareliaListPages.append(dic)

        except:
            if ( selectLowBlock == False):
                selectLowBlock = True
                i=0
                continue
            elif(selectLowBlock==True):
                break


    pagesIdList = []

    for item in kareliaListPages:
        objectUrl= "https://ru.wikivoyage.org/w/index.php?" + "title=Культурное_наследие_России/Карелия/" + item['name'] + "&action=info"


        request = requests.request('GET', objectUrl)  # response 200
        list_doc = fromstring(request.text)

        pageid = list_doc.cssselect('#mw-pageinfo-article-id > td:nth-child(2)')[0]

        pagesIdList.append(support.removeAllUseless(pageid.text))




    return pagesIdList

def fillListWiki():
    """
    обработка всех страниц по pageid
    возвращаем "0" если все данные были записаны в файлы


    :return 0:
    """

    allPagesId = getKareliaDistrictsWiki()


    listRegions = [] # список списков словарей

    try:
        os.mkdir("wikiFiles")
    except:
        print('file will be save in "WikiFiles"')
    os.chdir("wikiFiles")

    workbook = xlwt.Workbook()

    for pageid in allPagesId: # для каждой pageid

        f = wptools.page(wiki="ru.wikivoyage.org/w/api.php", pageid=pageid).get_parse()  # Получили class <str>

        sheet = workbook.add_sheet('list' + str(f.title.split("/")[2]))
        sheet.write(0, 0, "Id")
        sheet.write(0, 1, "Name")
        sheet.write(0, 2, "knid")
        sheet.write(0, 3, "newId")
        sheet.write(0, 4, "district")
        sheet.write(0, 5, "address")

        listOfData = [] # список словарей


        wikiText = f.wikitext.split("}}") # Если посмотреть структуру данных. Эти два символа отделяют записи


        countInNewRegister = 0

        #count был раньше перед item
        for item in wikiText:

            text = item.split("|") # разделяем запись на отдельные строки

            #print(text)

            name = ""
            knid = ""
            newid = ""
            inNewRegistry = False
            district = ""
            address = ""

            for i in text:

                if (re.match(r'name', i)):
                    name = i
                    continue

                elif (re.match(r'knid', i)):
                    if (re.match(r"knid-new", i[:8])):
                        newid = i
                        inNewRegistry = True
                        countInNewRegister += 1
                        continue
                    else:
                        knid = i
                        continue


                elif (re.match(r'district', i)):
                    district = i
                    continue

                elif (re.match(r'address', i)):
                    address = i
                    continue


            if (name==""):
                continue

            dictionary = {}

            # split после = и вторая часть. Мы отбрасывает ненужную часть строки. Т.к идентификатор будет в key словаря
            #dictionary['id'] = count
            dictionary['name'] = name.split("=")[1]
            dictionary['knid'] = support.removeAllUseless(knid).split("=")[1]
            dictionary['district'] = support.removeAllUseless(district).split("=")[1] # ������ ����� �����
            dictionary['address'] = address.split("=")[1]
            if (inNewRegistry==True):
                dictionary['inNewRegister'] = True
                dictionary['newid'] = support.removeAllUseless(newid).split("=")[1]
            elif (inNewRegistry==False):
                dictionary['newid'] = "No in new register"


            listOfData.append(dictionary)

        # sheet = workbook.add_sheet('list' + str(f.title.split("/")[2]))
        # sheet.write(0, 0, "Id")
        # sheet.write(0, 1, "Name")
        # sheet.write(0, 2, "knid")
        # sheet.write(0, 3, "newId")
        # sheet.write(0, 4, "district")
        # sheet.write(0, 5, "address")

        row = 1
        count = 0
        for item in listOfData:
            column = 0
            count += 1

            sheet.write(row, column, count)
            column += 1
            sheet.write(row, column, item['name'])
            column += 1
            sheet.write(row, column, item['knid'])
            column += 1
            sheet.write(row, column, item['newid'])
            column += 1
            sheet.write(row, column, item['district'])
            column += 1
            sheet.write(row, column, item['address'])
            column += 1

            row += 1

        # workbook.save('region_' + (f.title.split("/")[2]) + '_wiki.xls')
        workbook.save('wikiRegions.xls')
        countInNewRegister += 1

        # namefile = (f.title.split("/")[2])
        # count = 0
        # f = open(namefile, "w" )
        # for i in listOfData:
        #     count = count + 1
        #     f.write("\n______________________________________________\n\n")
        #     i['id'] = count
        #     f.write("%s\n" % i['id'])
        #     f.write("%s\n" % i['name'])
        #     f.write("%s\n" % i['knid'])
        #     f.write("%s\n" % i['newid'])
        #     f.write("%s\n" % i['district'])
        #     f.write("%s\n" % i['address'])
        #     f.write("\n______________________________________________")
        # f.write("\n====================================================")
        # f.write("%s\n" % "Отчет по региону")
        # f.write("%s\n" % "Всего объектов культурного наследия в регионе%s" %  str(count))
        # f.write("%s\n" % "Объектов которые занесены в новый реестр http://mkrf.ru/%s" %  str(countInNewRegister))
        # f.write("%s\n" % "Следует занести в новый реестр%s" %  str(count - countInNewRegister))
        #
        # f.close()


        """
        for i in listOfData:
            print("| Id: ", i['id'], '\n',
                  "\t| Name: ", i['name'], '\n',
                  "\t| � Object: ", i['knid'], '\n',
                  "\t| In new register: ", i['newid'], '\n',
                  "\t| District : ", i['district'], '\n',
                  "\t| Address : ", i['address'], '\n',
                  "______________________________________________________________")

        """

        listRegions.append(listOfData)

    return listRegions
