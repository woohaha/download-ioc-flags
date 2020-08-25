import requests

domain = 'https://en.wikipedia.org'


class Link:
    proxies = {
        'https': 'socks5://localhost:1080',
        'http': 'socks5://localhost:1080',
    }

    def __init__(self, link):
        self.link = link

    def getText(self) -> str:
        print(f'getting {self.link}')
        page = requests.get(self.link, proxies=self.proxies)
        return page.text

    def downloadContent(self, outputFile: str):
        r = requests.get(self.link, proxies=self.proxies, stream=True)

        if r.status_code == 200:
            with open(outputFile, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

    def __repr__(self):
        return self.link

    def __str__(self):
        return self.__repr__()


class Country:
    code: str
    name: str
    flag_page_link: Link
    flag_link: Link
    flag_file: str

    def export(self, writer):
        writer.writerow([self.name, self.code, self.flag_link])

    def __repr__(self):
        return f'{self.name},{self.code},{self.flag_link},{self.flag_file}'

    def __str__(self):
        return self.__repr__()
