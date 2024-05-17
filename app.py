import json
import time
import requests
from bs4 import BeautifulSoup


# # 首先从环境变量里获取
# host = os.getenv("one_host")
# torr_api = f"{os.getenv('torr_api')}/torrents"
# # 如果获取不到就走默认值
# host = host if host else "https://one.52378.fun"
# torr_api = torr_api if torr_api else "http://192.168.31.249:18090/torrents"
host = "https://one.52378.fun"
torr_api = "http://192.168.31.249:18090/torrents"


def get_page_list() -> list:
    """ 从网站主页获取详情页，返回一个详情页链接的列表 """
    with requests.get(host) as req:
        if req.status_code != 200:
            return

    soup = BeautifulSoup(req.text, "html.parser")
    page_list = soup.findAll(name="a", attrs={"class": "thumbnail-link"})
    page_list = [host + i.get("href") for i in page_list]
    return page_list


def get_magnet(url) -> str:
    """ 传入一个页面地址，获取该页的 magnet """
    with requests.get(url) as req:
        if req.status_code != 200:
            return

    soup = BeautifulSoup(req.text, "html.parser")
    try:
        magnet = soup.find(name="a", attrs={"class": "button is-primary is-fullwidth"}).get("href")
        image = soup.find(name="img", attrs={"class": "image"}).get("src")
        return magnet, image
    except:
        return


def add_download(magnet: str, image: str):
    """ 传入 magnet 链接，访问 torrserver api，添加内容 """
    payloads = {
        "action": "add",
        "category": "",
        "data": "",
        "hash": "",
        "link": magnet,
        "poster": image,
        "save_to_db": True,
        "title": ""
    }
    payloads = json.dumps(payloads)
    with requests.post(torr_api, data=payloads) as req:
        print(req.json())


def main_handle():
    """ 最后的任务处理 """
    pages = get_page_list()
    if pages:
        for i in pages:
            try:
                magnet, image = get_magnet(i)

                add_download(magnet, image)
            except:
                continue

if __name__ == "__main__":
    while True:
        main_handle()
        time.sleep(6 * 3600)
