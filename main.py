import time
import crawler

crawler.

url1 = 'https://scholar.google.com/scholar?start='
url2 = '&q=botnet+detection&hl=zh-CN&as_sdt=0,5&as_ylo=2015'
title_list = []
title_str = ''




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
    page_num = 1
    while title_num < 5000:
        print(str((page_num - 1) * 10 + 1) + '~' + str(page_num * 10) + '条:')
        crawl_page(title_num)
        title_num += 10
        page_num += 1
        time.sleep(1)

    word_count()
