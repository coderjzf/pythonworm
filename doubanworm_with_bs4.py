import json
import requests
from bs4 import BeautifulSoup


# def parse_one_page(html):
#     soup = BeautifulSoup(html, "html.parser")
#     resultsset_of_em = soup.find_all(name="em")
#     resultsset_of_title = soup.find_all(name="div", attrs={"class": "hd"})
#     resultsset_of_detail = soup.find_all(name="p", attrs={"class": ""})
#     resultsset_of_score = soup.find_all(attrs={"class": "rating_num"})
#     resultsset_of_quote_numbers = soup.find_all(name="span", attrs={"content": 10.0})
#     resultsset_of_quote = soup.find_all(attrs={"class": "inq"})
#
#     index = get_list(resultsset_of_em)  # 排名
#     title = get_title(resultsset_of_title)  # 电影名
#     quote = get_list(resultsset_of_quote)  # 一句话评价
#
#     quote_numbers = []  # 评价人数
#     for result in resultsset_of_quote_numbers:
#         quote_numbers.append(list(result.next_siblings)[1].string[:-2])
#
#     score = get_list(resultsset_of_score)  # 评分
#
#     actor = []  # 主创人员
#     releasetime = []  # 上映时间
#     for result in resultsset_of_detail:
#         for i, r in enumerate(result.children):
#             if i == 0:
#                 actor.append(r.string.strip())
#             elif i == 2:
#                 releasetime.append(r.string.strip())
#
#     # print(len(index))
#     # print(len(title))
#     # print(len(actor))
#     # print(len(releasetime))
#     # print(len(quote))
#     # print(len(quote_numbers))
#     # print(len(score))
#
#     films = []
#     for i in range(25):
#         f = (index[i], title[i], actor[i], releasetime[i], score[i], quote_numbers[i], quote[i])
#         films.append(f)
#
#     return films




def get_one_page(url, data):
    # 模拟get请求
    r = requests.get(url, params=data, timeout=2)
    # 如果请求成功,返回页面文本信息
    if r.status_code == 200:
        return r.text
    else:
        return None


# 解析网页,得到电影信息并写入文件
def parse_one_page_and_write_to_file(html):
    # 所有电影信息的标签
    content = BeautifulSoup(html, "html.parser").find(attrs={"class": "grid_view"})

    # 每部电影的信息都在1个li标签中
    for film in content.find_all('li'):
        # 电影排名
        index = film.find('em').string

        # 每个li标签包含2个a标签,第1个是详情页、第2个是电影名
        detail_src = film.find_all('a')[0].attrs['href']
        title = film.find_all('a')[1].find("span").string

        # 包含主演、上映时间、评分、评价人数的标签
        bd = film.find(attrs={"class": "bd"})

        # p标签实际包含3个子标签 第1个子标签为主创人员、第3个子标签为上映时间
        actors = list(bd.find('p').children)[0].strip()
        release_time = list(bd.find('p').children)[2].strip()

        # class为star的标签包含评分与评价人数
        score = bd.find(attrs={"class": "star"}).find(attrs={"class": "rating_num"}).string
        number_of_evaluators = bd.find(attrs={"class": "star"}).find_all('span')[3].string[:-3]

        # quote为电影的短评
        # 有的电影没有短评,所以在此做个判断
        quote = bd.find(attrs={"class": "quote"})
        if quote:
            quote = quote.find("span").string
        else:
            quote = ""

        # 一部电影要抓取的信息
        one_film = [index, detail_src, title, actors, release_time, score, number_of_evaluators, quote]

        # 将电影信息按部写入文件
        with open("douban250_2.txt", "a", encoding="utf-8") as file:
            file.write(json.dumps(one_film, ensure_ascii=False) + "\n")


def main():
    for i in range(10):
        # 共要抓取10个页面,start由0到225
        start = i * 25
        # 要抓取的网页
        url = "https://movie.douban.com/top250"
        # 参数信息
        data = {
            "start": start,
            "filter": ""
        }
        # 获取单页
        html = get_one_page(url, data)
        # 解析网页并将电影信息写入文件
        parse_one_page_and_write_to_file(html)

main()
