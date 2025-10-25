import typing
import requests
import time
from dataclasses import dataclass
from enum import Enum, auto
import base64
import hmac
import hashlib
from yandex_music.utils.sign_request import DEFAULT_SIGN_KEY
import re
from hashlib import md5


class Container(Enum):
    FLAC = auto()
    MP3 = auto()
    MP4 = auto()


class Codec(Enum):
    FLAC = auto()
    MP3 = auto()
    AAC = auto()


@dataclass
class FileFormat:
    container: Container
    codec: Codec

@dataclass
class CustomDownloadInfo:
    quality: str
    file_format: FileFormat
    urls: list[str]
    decryption_key: str
    bitrate: int

FILE_FORMAT_MAPPING = {
    "flac": FileFormat(Container.FLAC, Codec.FLAC),
    "flac-mp4": FileFormat(Container.MP4, Codec.FLAC),
    "mp3": FileFormat(Container.MP3, Codec.MP3),
    "aac": FileFormat(Container.MP4, Codec.AAC),
    "he-aac": FileFormat(Container.MP4, Codec.AAC),
    "aac-mp4": FileFormat(Container.MP4, Codec.AAC),
    "he-aac-mp4": FileFormat(Container.MP4, Codec.AAC),
}




SIGN_SALT = 'XGRlBW9FXlekgbPrRHuSiA' #Для генерации ссылки https://github.com/MarshalX/yandex-music-api/ на чьей основе я сделал скрипт оно было взял её из мобильного приложени/клиента для пк

def download_file(track_id: int, filename: str, token: str):
    """  "quality":
        LOW = "lq"
        NORMAL = "nq"
        HIGH = "hq"
        LOSSLESS = "lossless"
    """

    params = {
            "ts": int(time.time()),
            "quality": "lossless",
            "codecs": ",".join(FILE_FORMAT_MAPPING.keys()),
            "transports": "encraw"
        }

    header = {
        "Authorization": f"OAuth {token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
        "X-Yandex-Music-Client": "WindowsPhone/3.20"
    }

    hmac_sign = hmac.new(
            DEFAULT_SIGN_KEY.encode(),
            "".join(str(e) for e in params.values()).replace(",", "").encode(),
            hashlib.sha256
        )

    sign = base64.b64encode(hmac_sign.digest()).decode()[:-1]

    params["sign"] = sign

    response = requests.get(f"https://api.music.yandex.net/tracks/{track_id}/download-info", params=params, headers=header)
    print("\n", response.json())

    textresp = response.json()

    dlink = textresp['result'][0]['downloadInfoUrl']
    print("\n", "Тут бурем ссылку для скачивания:", dlink)

    downreq = requests.get(url=dlink)
    print("\n", "Из этого мы создаем ссылку для скачивания:", downreq.text)


    host = re.search(r"<host>(.*?)</host>", downreq.text).group(1)
    path = re.search(r"<path>(.*?)</path>", downreq.text).group(1)
    ts = re.search(r"<ts>(.*?)</ts>", downreq.text).group(1)
    region = re.search(r"<region>(.*?)</region>", downreq.text).group(1)
    s = re.search(r"<s>(.*?)</s>", downreq.text).group(1)
    sign = md5((SIGN_SALT + path[1::] + s).encode('UTF-8')).hexdigest()

    download_url = f'https://{host}/get-mp3/{sign}/{ts}{path}'
    print("\n", "Скачиваем отсюда:", download_url)


    file = requests.get(url=download_url)
    print("\n", "И сохраняем в:", filename)
    with open(f"{filename}", "wb") as f:

        f.write(file.content)


