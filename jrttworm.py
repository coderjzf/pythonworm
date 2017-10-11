# -*- coding: utf-8 -*-

# 利用requests+ajax获取今日头条街拍美图
# 打开今日头条官网,在右上角搜索框输入街拍,页面图片部分由ajax请求得到

import requests
import os
from hashlib import md5
from pathlib import Path


# 模拟发送ajax请求
def get_one_page(url, params):
    try:
        # 使用requests库发送get请求
        result = requests.get(url, params=params, timeout=2)
        if result.status_code == 200:
            return result.json()
    except requests.ConnectionError as e:
        print(e.reson)


# 解析返回的json数据的生成器
def parse_one_page(json):
    if json.get("data"):
        for item in json.get("data"):
            # 获取标题
            title = item.get('title')
            # 获取含有图片url的列表
            images = item.get('image_detail')
            # 有部分数据没有image_detail键
            if not images:
                continue
            for image in images:
                yield {
                    "title": title,
                    "image": image.get("url")
                }


# 下载并保存图片
def save_images(item):
    path = Path("f:\\images")
    # 以标题名作为文件夹名
    directory = os.path.join(path, item.get("title"))
    if not os.path.exists(directory):
        os.mkdir(directory)

    try:
        # 下载图片
        response = requests.get(item.get("image"))
        if response.status_code == 200:
            # 图片二进制内容的md5值来作为文件名,同一个标题的图片放入同一个文件夹中
            file_path = "{0}/{1}.{2}".format(directory, md5(response.content).hexdigest(), "jpg")
            if os.path.exists(file_path):
                print(file_path + " already download!")
            else:
                # 保存图片
                with open(file_path, "wb") as file:
                    file.write(response.content)
        else:
            print("can't download image!")
    except requests.ConnectionError as e:
        print("failed to save image!")


# 主方法固定写法
if __name__ == '__main__':

    for i in range(2):
        # 通过offset来分页
        offset = i * 20
        # 要抓取的url
        url = "http://www.toutiao.com/search_content/?"
        # 参数列表
        params = {
            "offset": offset,
            "format": "json",
            "keyword": "街拍",
            "autoload": "true",
            "count": 20,
            "cur_tab": 1
        }

        json = get_one_page(url, params)
        for item in parse_one_page(json):
            print(item)
            save_images(item)
