import requests
import re
import time
import jieba

# you need to fill this part
headers = {

}

proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}

url1 = 'https://scholar.google.com/scholar?start='
url2 = '&q=botnet+detection&hl=zh-CN&as_sdt=0,5&as_ylo=2016'
title_list = []
title_str = ''


def crawl_page(num):
    global title_str
    my_url = url1 + str(num) + url2
    response = requests.get(my_url, headers=headers, proxies=proxies)

    text = response.text

    res_list = re.findall('gs_rt">(.*?)</h3>', text, re.S)
    print(len(res_list))

    with open('title.txt', 'a') as f:
        for each in res_list:
            title = re.findall('ei.+">(.*?)</a>', each, re.S)
            if len(title) == 0:
                continue
            title = title[0]
            title = title.replace('<b>', '').replace('</b>', '')
            title_str += title
            title_str += ' '
            f.write(title + '\n')
            print(title + '\n')


def word_count():
    words_dict = {}
    words_list = title_str.split(' ')
    for word in words_list:
        words_dict.setdefault(word, 0)
        words_dict[word] += 1
    word_sorted_list = sorted(words_dict.items(), key=lambda d: d[1], reverse=True)
    print(words_dict)
    print(word_sorted_list)
    print('-------------------------------------------------')
    for word in word_sorted_list:
        print(word[0] + ': ' + str(word[1]))


if __name__ == '__main__':
    title_num = 0
    while title_num < 500:
        crawl_page(title_num)
        title_num += 10
        time.sleep(1)

    word_count()
