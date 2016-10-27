import requests
import re
from bs4 import BeautifulSoup
import leancloud
from leancloud import Object

leancloud.init('oHXUIopsgLvYUElgyRbUuw8o-gzGzoHsz', 'WGGuqAPWgvY0yji7P8cOa9d2')


class PaperInfo(Object):
    pass

# you need to fill this part
headers = {
    'referer': 'https://www.google.com/',
    'upgrade-insecure-requests': '1',
    'cache-control': 'max-age=0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0'
              '.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'x-client-data': 'CJK2yQEIprbJAQjBtskBCKOZygEIqZ3KAQ==',

    'user-agent': '',
    'cookie': ''
}

proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}




def get_info(regular, string):
    info = re.findall(regular, string, re.S)
    if len(info) != 0:
        info = info[0].strip()
    else:
        info = ''
    return info


def crawl_page(keywords, start_num, s_year, e_year):
    keywords = keywords.replace(' ', '+')
    my_url = 'https://scholar.google.com/scholar?start=%s&q=%s&hl=' \
             'zh-CN&as_sdt=0,5&as_ylo=%s&as_yhi=%s&as_vis=1'
    my_url = (my_url % (str(start_num), keywords, str(s_year), str(e_year)))
    print(my_url)
    response = requests.get(my_url, headers=headers, timeout=20, proxies=proxies)
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    cells = soup.find_all('div', class_='gs_ri', id=False)
    print(len(cells))
    for each in cells:

        # 获取排名
        rank = int(start_num + 1 + cells.index(each))
        print(rank)

        each = str(each)
        print(each)

        # 获取论文标题
        title = get_info('class="gs_rt".*?">(.*?)</a>', each)
        title = title.replace('<b>', '').replace('</b>', '')
        # print(title)
        if 'href' in title:
            title = get_info('href.*?>(.*?)$', title)
        print(title)

        # 获取论文作者
        author = get_info('class="gs_a"(.*?)</div>', each)
        print(author)
        if ',' in author:
            author = get_info('>(.*?),', author)
        else:
            author = get_info('>(.*?) -', author)
        if 'href' in author:
            author = get_info('href.*?>(.*?)</a>', author)
        if ' -' in author:
            author = get_info('(.*?) -', author)
        print(author)

        # 获取被引用次数
        cited_num = get_info('被引用次数：(.*?)</a>', each)
        cited_num = 0 if cited_num == '' else int(cited_num)
        print(cited_num)

        # 获取年份
        year = get_info('</h3>.*?([0-9]+) -', each)
        year = 0 if year == '' else int(year)
        print(year)

        # 判断当前paper是否存在，如果标题、关键词、开始时间、结束时间都相同则认为存在，否则不存在进行插入操作。
        # 若存在，如果引用数或排名发生变化则进行更新
        exist = False
        try:
            query = leancloud.Query('PaperInfo')
            query_list = query.equal_to('title', title).find()
            for paper in query_list:
                if paper.get('keywords') == keywords and paper.get('s_year') == s_year and \
                        paper.get('e_year') == e_year:
                    exist = True
                    if paper.get('cited_num') != cited_num or paper.get('rank') != rank or \
                            paper.get('author') != author or paper.get('year') != year:
                        paper_id = paper.id
                        paper_info = PaperInfo()
                        paper_info.create_without_data(paper_id)
                        paper_info.set('cited_num', cited_num)
                        paper_info.set('rank', rank)
                        paper_info.set('author', author)
                        paper_info.set('year', year)
                        paper_info.save()

        except Exception as e:
            print(e)
        # print(len(query_list))
        if not exist:
            paper_info = PaperInfo()
            paper_info.set('title', title)
            paper_info.set('author', author)
            paper_info.set('year', year)
            paper_info.set('cited_num', cited_num)
            paper_info.set('keywords', keywords)
            paper_info.set('s_year', s_year)
            paper_info.set('e_year', e_year)
            paper_info.set('rank', rank)
            paper_info.save()
        print('\n')

num = 680
while num < 10000:
    crawl_page('botnet', num, 2010, 2016)
    num += 10
