from os.path import basename

from qiniu import Auth, put_file

from model import Link


class QiniuProvider:
    access_key = ''
    secret_key = ''
    bucket = ''
    domain = ''

    def __init__(self):
        self.q = Auth(self.access_key, self.secret_key)

    def upload(self, filePath: str) -> Link:
        remoteFileName = basename(filePath)
        remoteDir = 'flag'
        key = f'{remoteDir}/{remoteFileName}'
        token = self.q.upload_token(bucket=self.bucket, key=key)
        ret, info = put_file(token, key, filePath)
        url = f'https://{self.domain}/{ret["key"]}'
        print(f'uploaded to {url}')
        return Link(url)
