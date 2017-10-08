import re
import requests
import time


# 获取网页
def get_one_page(url, data):
    r = requests.get(url, params=data, timeout=2)
    if r.status_code == 200:
        return r.text
    else:
        return None

        # NETWORK_STATUS = True
        # while not NETWORK_STATUS:
        #     try:
        #         r = requests.get(url, params=data, timeout=2)
        #     except requests.exceptions.ConnectionError:
        #         print("network is not good!")
        #         NETWORK_STATUS = False
        #     else:
        #         if r.status_code == 200:
        #             return r.text
        #         else:
        #             return None


# 解析网页
def parse_one_page(html):
    # 利用正则表达式进行匹配
    pattern = re.compile(r'<li>.*?<em class="">(.*?)</em>.*?' +
                         r'img.*?alt="(.*?)".*?' +
                         r'bd.*?p.*?>(.*?)</p>.*?' +
                         r'v:average.*?>(.*?)</span>.*?' +
                         r'inq.*?>(.*?)</span>.*?</li>', re.S)
    results = re.findall(pattern, html)
    # 解析列表
    for result in results:
        yield {
            "index": result[0],
            "name": result[1],
            "detail": result[2].strip(),
            "score": result[3],
            "quote": result[4]
        }


# 写入文件
def write_to_file(item):
    with open("douban250.txt", "a", encoding="utf-8") as file:
        file.write(str(item) + "\n")

# 主方法
def main():
    for i in range(10):
        start = i * 25
        data = {
            "start": start,
            "filter": ""
        }
        url = "https://movie.douban.com/top250"
        html = get_one_page(url, data)
        for item in parse_one_page(html):
            write_to_file(str(item) + "\n")
        time.sleep(1)


main()
