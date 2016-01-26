# coding=utf-8
__author__ = 'tzq'
import urllib2
import config
import sys
import chardet

class HttpHelper:
    def __init__(self):
        # self.tool = tool.Tool()
        self.tool = ''
        
    # 解析页面
    def getHtml(self, url):
        req = urllib2.Request(
            url=url,
            headers=config.HEADERS
        )
        try:
            myResponse = urllib2.urlopen(req).read()
            typeEncode = sys.getfilesystemencoding()  ##系统默认编码

            infoencode = chardet.detect(myResponse).get('encoding', 'gb2312')  ##通过第3方模块来自动提取网页的编码

            html = myResponse.decode(infoencode, 'ignore').encode('utf-8')  ##先转换成unicode编码，然后转换系统编码输出
            return html
        except:
            print "Unexpected error:", sys.exc_info()[2]
            return None


# parser = HttpHelper()

# print parser.getHtml('http://www.zhonghe.cn/news.asp?Mode=%B9%AB%CB%BE%D0%C2%CE%C5')
