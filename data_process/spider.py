"""
爬
"""
from urllib import request, parse
from fake_useragent import UserAgent
import time, random


class TiebaSpider:
    def __init__(self):
        self.url = 'http://tieba.baidu.com/f?kw={}&pn={}'

    # 获取url
    def get_url(self, kw, pn):
        kw = parse.quote('kw')
        url = self.url.format(kw, pn)
        print(url)
        return url

    # 获取User-Agent
    def get_useragent(self):
        ua = UserAgent()
        return ua.random

    # 保存html页面
    def write_html(self, html, filename):
        print(filename, html)

    # 获取html
    def get_html(self, url):
        headers = {'User-Agent': self.get_useragent()}
        req = request.Request(url, headers=headers)
        res = request.urlopen(req)
        html = res.read().decode()
        return html

    # 运行主程序
    def run(self,kw,start,end):
        for i in range(start, end + 1):
            pn = (i - 1) * 50
            url = self.get_url(kw, pn)
            html = self.get_html(url)
            filename = '{}-第{}.html'.format(kw, i)
            self.write_html(html, filename)
            print(filename, ' 完成啦')
            time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    kw = input('请输入贴吧:')
    start = int(input('请输入起始页:'))
    end = int(input('请输入结束页:'))
    tieba = TiebaSpider()
    while True:
        try:
            tieba.run(kw,start,end)
            break
        except Exception as e:
            print(e)
            time.sleep(0.5)