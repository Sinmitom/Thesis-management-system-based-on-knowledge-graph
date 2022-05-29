import requests
import random
import urllib.parse
import time
import urllib
import urllib.request
import urllib.parse
import urllib.error
from lxml import etree
from utils import *

USER_AGENT = [
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
    "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0",
]


# 获取user agent
def get_ua():
    return USER_AGENT[random.randint(0, len(USER_AGENT) - 1)]


class Crawler:
    # 睡眠时长
    __time_sleep = 0.5
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {'User-Agent': get_ua(), 'Cookie': ''}
    __total_page = 0
    __word = None

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.database = None
        self.time_sleep = t
        self.signal = None

    # 开始获取
    def get_paper_info(self, word):
        base_url = 'https://xueshu.baidu.com/s?wd={}&pn={}&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&sc_hit=1'
        word = urllib.parse.quote(word)
        for i in range(self.__total_page):
            url = base_url.format(word, i * 20)
            self.get_one_page(url)
            time.sleep(3)

    def get_one_page(self, url):
        html = requests.get(url=url, headers=self.headers).text
        html = html.replace('<em>', '')
        html = html.replace('</em>', '')
        html = html.replace('\n', '').replace('\r', '')
        html = etree.HTML(html)
        titles = html.xpath('//*[@class="result sc_default_result xpath-log"]/div[1]/h3/a/text()')
        urls = html.xpath('//*[@class="result sc_default_result xpath-log"]/div[1]/h3/a/@href')
        for i in range(len(urls)):
            data = {}
            try:
                data["authors"], data["year"], data["cites"], data["key_words"] = self.get_one_paper(urls[i])
                data["title"] = titles[i]
                data["url"] = urls[i]
                data["word"] = self.__word
                if self.database.insert(data):
                    self.database.insert_connect(data)
                self.signal.text_print.emit('已爬取论文 + 1')
            except Exception as e:
                print(e)
                print(urls[i])
            time.sleep(0.1)

    def get_one_paper(self, url):
        html = requests.get(url=url, headers=self.headers).text
        html = etree.HTML(html)
        authors = html.xpath('//*[@id="dtl_l"]/div[1]/div[1]/div[2]/p[2]/span/a/text()')
        authors = ",".join(authors)
        year = html.xpath("//p[@data-click=\"{\'button_tp':'year\'}\"]/text()")[0]
        year = int(year.replace('\n', '').replace('\r', ''))
        cites = html.xpath('//*[@id="dtl_l"]/div[1]/div[1]/div[6]/p[2]/a/text()')
        if len(cites) > 0:
            cites = int(cites[0].replace('\n', '').replace('\r', ''))
        else:
            cites = 0
        key_words = html.xpath('//*[@id="dtl_l"]/div[1]/div[1]/div[4]/p[2]/span/a/text()')
        words = []
        for item in key_words:
            item = item.replace('；', '/')
            item = item.replace(';', '/')
            item = item.split('/')
            item = [i.strip() for i in item]
            words.extend(item)
        if len(words) > 7:
            words = words[:6]
        words = ",".join(words)
        return authors, year, cites, words

    def start(self, word, total_page=1, signal=None, database=None):
        """
        爬虫入口
        :param database: 数据库
        :param signal: 信号量
        :param word: 抓取的关键词
        :return:
        """
        self.signal = signal
        self.database = database
        self.__total_page = total_page
        self.__word = word
        self.get_paper_info(word)


if __name__ == '__main__':
    # spider = Crawler()
    # word = '狗'
    # spider.start(word)
    url = 'https://xueshu.baidu.com/s?wd=%E7%88%AC%E8%99%AB&pn=20&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&sc_hit=1'
    spider = Crawler()
    db = PaperData()
    spider.start('yolo', 3, database=db)
    # spider.get_one_paper(
    #     'https://xueshu.baidu.com/usercenter/paper/show?paperid=57141e1a1f4600f73570c8e2935a0438&site=xueshu_se')
    # spider.get_one_page(url=url)
    # headers = {'User-Agent': get_ua()}
    # data = requests.get(url, headers)
    # cookie = requests.utils.dict_from_cookiejar(data.cookies)
    # print(cookie)
    # print(data.text)
