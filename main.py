import os
from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from SQLExporter import SQLExporter
from model import Country, Link, domain, Flag
from upload import QiniuProvider


def parseTable(page: str) -> List[Country]:
    list = []
    soup = BeautifulSoup(page, "html.parser")
    codeTable = soup.find_all('table', attrs={'class': 'wikitable'})[0].find_all('tr')
    for countryTable in codeTable:
        country = Country()
        try:
            country.code = countryTable.span.text
            country.name = countryTable.a.text
            # country.flag_page_link = Flag(domain + countryTable.a['href']) # 需要svg格式时
            country.flag_page_link = Flag("https:" + countryTable.img['src'].replace("22px", "480px")) # 需要png格式
            list.append(country)
        except AttributeError:
            pass
    return list



class ExecutorParams:
    q: QiniuProvider
    country: Country

    def __init__(self, q: QiniuProvider, country: Country, writer):
        self.q = q
        self.country = country
        self.writer = writer


def executor(param: ExecutorParams):
    country = param.country
    q = param.q
    writer = param.writer
    country.flag_file = f'./flags/{country.code}.png'

    if not os.path.exists(country.flag_file):
        # country.flag_page_link.downloadSVG(
        #     country.flag_file)
        country.flag_page_link.downloadPNG(
            country.flag_file)

    country.flag_link = q.upload(country.flag_file)
    country.export(writer)

    return country.name


def main():
    Q = QiniuProvider()
    countries = parseTable(Link(f'{domain}/wiki/List_of_IOC_country_codes').getText())
    beginTime = datetime.now()
    with ThreadPoolExecutor(max_workers=10) as pool:
        allTasks = []

        sqlFile = open('countryList.sql', 'w', encoding="utf-8")
        sqlWriter = SQLExporter(sqlFile, 'nationality', ['name', 'code', 'flag'])

        for country in countries:
            print(f'graping {country.name}...')
            allTasks.append(pool.submit(executor, ExecutorParams(q=Q, country=country, writer=sqlWriter)))

        for task in as_completed(allTasks):
            print(f'{task.result()} downloaded.')

        sqlFile.close()

        endTime = datetime.now()

        print(f'run time: {endTime - beginTime}')


if __name__ == '__main__':
    main()
