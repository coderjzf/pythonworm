import xlwt
import requests
from bs4 import BeautifulSoup

wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
sh = wb.add_sheet("豆瓣电影Top250", cell_overwrite_ok=True)
sh.write(0, 0, "电影排名")
sh.write(0, 1, "电影详情连接")
sh.write(0, 2, "电影名")
sh.write(0, 3, "主创人员")
sh.write(0, 4, "上映时间")
sh.write(0, 5, "评分")
sh.write(0, 6, "评价人数")
sh.write(0, 7, "短评")

n = 1


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

        global n

        sh.write(n, 0, index)
        sh.write(n, 1, detail_src)
        sh.write(n, 2, title)
        sh.write(n, 3, actors)
        sh.write(n, 4, release_time)
        sh.write(n, 5, score)
        sh.write(n, 6, number_of_evaluators)
        sh.write(n, 7, quote)

        n = n + 1


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
    wb.save("豆瓣电影Top250.xls")


main()
