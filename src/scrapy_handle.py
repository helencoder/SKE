#coding=utf-8

import urllib
import requests

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

#处理文本获取()
def get_html_data(url):
    # 进行文本抓取
    response = requests.get(url)
    if response.status_code != 200:
        return False
    else:
        return response.text

# 此下面的语句被import引入后不会执行
if __name__ == "__main__":
    url = ''
    getHtml(url)
    # get_html_data(url)