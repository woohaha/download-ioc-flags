from typing import List

from bs4 import BeautifulSoup

from model import Country, Link, domain


def parseTable(page: str) -> List[Country]:
    list = []
    soup = BeautifulSoup(page, "html.parser")
    codeTable = soup.find_all('table', attrs={'class': 'wikitable'})[0].find_all('tr')
    for countryTable in codeTable:
        country = Country()
        try:
            country.code = countryTable.span.text
            country.name = countryTable.a.text
            country.flag_page_link = Link(domain + countryTable.a['href'])
            list.append(country)
        except AttributeError:
            pass
    return list


def getFlagDetailFromDetailPage(page: str) -> Link:
    soup = BeautifulSoup(page, "html.parser")
    image = soup.find('a', attrs={'class': 'image'})
    return Link(domain + image['href'])


def getImageLinkFromFlagPage(page: str) -> Link:
    soup = BeautifulSoup(page, "html.parser")
    return Link('https:' + soup.find('div', attrs={'class': 'fullMedia'}).find('a')['href'])
