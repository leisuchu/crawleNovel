"""
    爬虫测试
    爬取biquge小说，小阁老
    经济允许的话，请支持正版
"""
import re
import threading
from urllib import request
from io import BytesIO
import gzip
from filetools import write_file


class Spider():
    novel_name = '小阁老'
    baseUrl = 'http://www.xbiquge.la'

    # 小说第一章网址
    # 爬取其他小说时换成相应的第一章网址
    url = baseUrl + '/28/28056/13639427.html'

    is_time_out = False

    # 超时时间，单位秒
    time_out_var = 3

    # 爬取原html内容
    def __fetch_content(self, url):
        res = request.urlopen(url or Spider.url, data=None, timeout=3)
        # 读出来的是字节码,有可能是gzip压缩过的
        gzip_html = res.read()

        try:
            buff = BytesIO(gzip_html)
            f = gzip.GzipFile(fileobj=buff)
            htmls = f.read().decode('utf-8')
        except:
            htmls = str(gzip_html, encoding='utf-8')

        return htmls

    def parse_biquge(self, url):

        # 处理每一次的句子
        def get_content_map(ori_content):
            sub_content = re.search('&nbsp;&nbsp;&nbsp;&nbsp;(.*)<br />', ori_content)
            return ' ' * 4 + sub_content.group(1)

        htmls = self.__fetch_content(url)

        # 获取标题
        title_groups = re.search('<h1>(.*)</h1>', htmls)
        novel_title = title_groups.group(1)
        novel_content_groups = re.search('<div id="content">(.*)</div>', htmls)

        # 获取正文
        sentence = re.findall('&nbsp;&nbsp;&nbsp;&nbsp;.*?<br />', novel_content_groups.group(1))
        sentence = map(get_content_map, sentence)
        novel_content = novel_title + '\n' + '\n'.join(list(sentence))

        # 获取下一章节的地址
        next_chapter_ori = re.search(' &rarr; <a href="(.*)">下一章</a>', htmls)
        next_chapter = next_chapter_ori.group(1)

        isLastPage = re.search('.*\.html', next_chapter)

        next_url = 'isLastPage' if isLastPage is None else Spider.baseUrl + next_chapter
        return novel_content, next_url

    # 爬取固定章节的小说
    def fetch_by_num(self, chapter_num):
        next_url = Spider.url
        for i in range(chapter_num):
            novel_content, next_chapter_url = self.parse_biquge(next_url)
            write_file(novel_content, '小阁老')
            if next_chapter_url == 'isLastPage':
                break
            next_url = next_chapter_url

    # 爬取所有小说内容
    def fetch_all(self):
        next_url = Spider.url
        while True:
            if self.is_time_out:
                print('已超时！超时时间：', self.time_out_var, '秒')
                break
            novel_content, next_chapter_url = self.parse_biquge(next_url)
            write_file(novel_content, Spider.novel_name)
            if next_chapter_url == 'isLastPage':
                break
            next_url = next_chapter_url

    # 设置超时，防止死循环
    def run_timer(self, out_time=None):
        self.time_out_var = self.time_out_var if out_time is None else out_time

        def stop_fetch():
            self.is_time_out = True

        timer = threading.Timer(self.time_out_var, stop_fetch)
        timer.start()
        self.fetch_all()


spider = Spider()

# 测试10超时的爬取
spider.run_timer(10)
