import os
from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

from SQLExporter import SQLExporter
from model import Country, Link, domain
from parser import parseTable, getFlagDetailFromDetailPage, getImageLinkFromFlagPage
from upload import QiniuProvider


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
    country.flag_file = f'./flags/{country.code}.svg'

    if not os.path.exists(country.flag_file):
        getImageLinkFromFlagPage(
            getFlagDetailFromDetailPage(
                country.flag_page_link.getText()
            ).getText()
        ).downloadContent(
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

        # csvfile = open('countryList.csv', 'w', encoding="utf-8")
        # csvWriter = csv.writer(csvfile)
        #
        sqlFile = open('countryList.sql', 'w', encoding="utf-8")
        sqlWriter = SQLExporter(sqlFile, 'nationality', ['name', 'code', 'flag'])

        for country in countries:
            print(f'graping {country.name}...')
            allTasks.append(pool.submit(executor, ExecutorParams(q=Q, country=country, writer=sqlWriter)))

        for task in as_completed(allTasks):
            print(f'{task.result()} downloaded.')

        # csvfile.close()
        sqlFile.close()

        endTime = datetime.now()

        print(f'run time: {endTime - beginTime}')


if __name__ == '__main__':
    main()
