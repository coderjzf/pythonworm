from bs4 import BeautifulSoup
import re

soup = BeautifulSoup("<html><body><b class='title' id='1'>jiazhengfneg</b></body></html>", 'html.parser')

# BeautifulSoup中的Tag类代表Html或者Xml中的tag,Tag类有很多属性和方法
# 以标准格式输出
print(soup.prettify())
# 获取标签
print(soup.b)
# 获取名字
print(soup.b.name)
# 对属性的操作与对字典的操作相同
print(soup.b['id'])
soup.b['id'] = 2
# 获取多值属性会得到一个列表 如class属性
print(soup.b['class'])
# del soup.b['class']

# BeautifulSoup用NavigableString类来表示Tag中的字符串
print(type(soup.b.string))
print(soup.b.string)
# Tag中的字符串不能被编辑,但是可以被替换
soup.b.string.replace_with('hhh i\'m jiazhengfeng')
print(soup.b)

# BeautifulSoup对象并不是真正的Html或Xml的tag,它没有name和attribute属性,但是可以查看它的.name
print(soup.name)

soup = BeautifulSoup("<html><body><b><!--Hey! I\'m JiaZhengFeng--></b></body></html>", 'html.parser')
# comment对象是一个特殊的NavigableString对象,代表注释部分
print(type(soup.b.string))  # <class 'bs4.element.Comment'>
print(soup.b.string)  # Hey! I'm JiaZhengFeng

'''
遍历文档树
'''

html_doc = """
<html><head><title>The Dormouse's story</title></head>

<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
soup = BeautifulSoup(html_doc, "html.parser")
# 获取子节点

# 通过tag的名字获取子节点,即.加上标签名字.子节点可能是tag也可能是字符串
print(soup.head)
print(soup.title)
# 通过.加上标签名字的方法只能获取当前名字的第一个标签
print(soup.p)

# 通过contents属性  .contents将tag的所有子节点以列表的形式返回
print(soup.head.contents)
print(soup.head.title.contents)
# 字符串没有contents属性

# 通过children属性返回的生成器,可以对tag的子节点进行遍历
for i, child in enumerate(soup.head.children):
    print(i, child)

# 通过contents属性和children属性返回的是tag的直接子节点
# 通过tag的descendants属性返回tag的所有子孙节点
for child in soup.head.descendants:
    print(child)

# 如果tag只有一个NavigableString类型的子节点或者tag只有一个子节点,可以
print(soup.head.string)
print(soup.head.title.string)

# 获取父节点

# 通过parent属性获取直接父节点
print(soup.title.parent)
# tag的字符串节点也有父节点
print(soup.title.string.parent)

# 通过parents属性返回tag的所有父节点
a = soup.a
for parent in a.parents:
    if parent:
        print(parent.name)
    else:
        print("None")

'''
搜索文档树
'''

# find_all方法,传入各种类型的过滤器,判断是否符合过滤器的条件,并返回匹配内容.过滤器可以是以下类型


# 字符串
print(soup.find_all('b'))  # 返回bs4.element.ResultSet类型
# 正则表达式
for tag in soup.find_all(re.compile('t')):  # 返回所有名字中包含t字符的标签
    print(tag.name)
# 列表
print(soup.find_all(['a', 'b']))  # 返回与列表中任意元素相匹配的内容返回
# 方法

# find_all( name , attrs , recursive , text , **kwargs )
# name参数,查找索所有名字为name的tag,不包括字符串,可以使用任意类型的过滤器

# keyword参数,如果实参名不是内置的形参名,则搜索时把该参数当作tag的属性值来搜索.属性的搜索可以使用索引除了方法以外的过滤器类型
print(soup.find_all(id=re.compile('link')))

# 有些tag的属性不能使用keyword参数搜索.但是可以使用attrs参数传入一个字典来搜索
data_soup = BeautifulSoup('<div data-foo="value">foo!</div>', 'html.parser')
print(data_soup.find_all(attrs={"data-foo": "value"}))

# 按css搜索,即按class名搜索.由于class为python中的关键字,所以使用class_,可以使用任何类型的过滤器
print(soup.find_all(class_='sister'))

# 按字符串内容搜索 通过text参数
print(soup.find_all(text='Elsie'))  # 返回包含符合条件的字符串的ResultSet

# 使用limit参数限制返回结果的数量
print(soup.find_all(class_='sister', limit=2))

# 使用recursive参数限制仅搜索直接子节点
print(soup.find_all('title', recursive=False))

# 像调用find_all一样来调用tag
# BeautifulSoup、Tag对象可以被当作find_all方法来使用
# soup('a') 等价于 soup.find_all('a')


# find方法与find_all方法用法相同,区别在于find方法只返回一个结果
# soup.head.title 的原理就是 soup.find('head').find('title'))
