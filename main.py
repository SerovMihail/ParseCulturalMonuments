# -*- coding: utf-8 -*-


import supportingFunc as s


def main():

     s.checkLastUpdate()
     s.compare2files('wikiRegions.xls', 'reg_10_mkrf.xls')

if __name__ == '__main__':
    main()
