import hashlib
import time
import re
from log import logger

import httpx
from httpx._exceptions import RequestError

class get_biliuserinfo():
    def __init__(self, mid: int):
        self.mid = str(mid)


    def _generator(self):
        req = httpx.get("https://api.bilibili.com/x/web-interface/nav")
        if not req.status_code != 400:
            raise RequestError("请求数据失败")
        con = req.json()
        img_url = con["data"]["wbi_img"]["img_url"]
        sub_url = con["data"]["wbi_img"]["sub_url"]
        # 伪装成了url，提取其中文件名
        re_rule = r'wbi/(.*?).png'
        img_key = "".join(re.findall(re_rule, img_url))
        sub_key = "".join(re.findall(re_rule, sub_url))

        n = img_key + sub_key  # 拼接两串值
        array = list(n)  # 拆分转arr
        order = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5,
                 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7,
                 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54,
                 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52]
        salt = ''.join([array[i] for i in order])[:32]  # 按照特定顺序混淆并取前32位
        return salt

    def _w_rid(self):  # 每次请求生成w_rid参数
        salt = self._generator()
        if (time.perf_counter() - time.perf_counter()) > 24 * 60 * 60:  # 一天更新一次salt
            salt = self._generator()  # 尾部加盐，根据imgKey,subKey混淆得出
        wts = str(int(time.time()))  # 时间戳
        b = "mid=" + self.mid + "&platform=web&token=&web_location=1550101"
        a = b + "&wts=" + wts + salt  # mid + platform + token + web_location + 时间戳wts + 一个固定值
        return hashlib.md5(a.encode(encoding='utf-8')).hexdigest()


    def get(self):
        API = {
            "url": "https://api.bilibili.com/x/space/wbi/acc/info",
            "params": {
                "mid": self.mid,
                "token": '',
                "platform": "web",
                "web_location": 1550101,
                "w_rid": self._w_rid(),
                "wts": str(int(time.time()))
            }
        }
        DEFAULT_HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41",
            "Referer": "https://www.bilibili.com/" + self.mid,
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": "https://space.bilibili.com",

        }
        t = time.localtime()
        req = httpx.request("GET", **API, headers=DEFAULT_HEADERS)
        logger.info(req)
        return req

if __name__ == '__main__':
    g = get_biliuserinfo(233114959)
    print(g.get().json())
    import json
    with open(file='t.json', mode='w+', encoding='utf-8') as f:
        f.write(json.dumps(g.get().json()))
    print(g.get().url)


