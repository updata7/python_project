#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
import execjs
import splinter
from splinter.browser import Browser
from splinter.driver.webdriver.chrome import Options, Chrome
from urllib import urlopen
import  os
from tqdm import tqdm
import re

class dyVideoDown(object):
    '下载抖音无水印视频,模拟post请求'
    def __init__(self):
        self.url = 'http://dy.wsdr8.cn/douyin.php'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': self.user_agent,
        }
    def get_video_url(self, dy_url):
        # r是随机数
        r = execjs.eval('Math.random().toString(10).substring(2)')
        # s是根据随机数r一定的规则生成的(太长不想分析， 直接用execjs这个库直接跑js代码)
        s = self.generateStr('{}@{}'.format(dy_url, r))
        sing = 1#'%s|%d' % (str(r), s)    # 只要每次传的都不一样就可以
        data = {
            'url': dy_url,
            'sing': sing
        }
        req = requests.Session()
        #data = json.dumps(data).encode('utf-8')
        res = req.post(self.url, headers=self.headers, data=data)
        r = res.json()
        print u"====%s" % r['msg']
        if r['code'] == '1':
            print u'--- %s' % r['fxw_url']
            url = r['fxw_url']
            if not url:
                return

            if re.search('url=http', url):
                url = re.sub(r'http.*url=', '', url)
            print '********** ', url
            return url

    def download(self, url, filename, name):
        """
        :param url: 视频直接链接
        :param filename: 保存文件名
        :param name: 进度条内容
        :return:
        """
        file_size = int(urlopen(url).info().get('Content-Length', -1))
        print file_size
        print '=== file_size(%s)' % file_size

        if os.path.exists(filename):
            os.remove(filename)
        first_byte = 0
        if first_byte >= file_size:
            print 'first_byte(%s) >= file_size(%s)' %(first_byte, file_size)
            return file_size
        header = {
            # "Range": "bytes=%s-%s" % (first_byte, file_size),
            "Range": "bytes=0-",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=name)
        req = requests.get(url, headers=header, stream=True)
        with(open(filename, 'wb')) as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.close()
        return file_size

    # 生成参数s
    def generateStr(self, a):
        js = '''
     test = function(a) {
     var c = function() {
     for (var d = 0,
     f = new Array(256), g = 0; 256 != g; ++g) {
     d = g,
     d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
     d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
     d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
     d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
     d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
     d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
     d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
     d = 1 & d ? -306674912 ^ d >>> 1 : d >>> 1,
     f[g] = d
     }
     return "undefined" != typeof Int32Array ? new Int32Array(f) : f
     } (),
     b = function(g) {
     for (var j, k, h = -1,
     f = 0,
     d = g.length; f < d;) {
     j = g.charCodeAt(f++),
     j < 128 ? h = h >>> 8 ^ c[255 & (h ^ j)] : j < 2048 ? (h = h >>> 8 ^ c[255 & (h ^ (192 | j >> 6 & 31))], h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & j))]) : j >= 55296 && j < 57344 ? (j = (1023 & j) + 64, k = 1023 & g.charCodeAt(f++), h = h >>> 8 ^ c[255 & (h ^ (240 | j >> 8 & 7))], h = h >>> 8 ^ c[255 & (h ^ (128 | j >> 2 & 63))], h = h >>> 8 ^ c[255 & (h ^ (128 | k >> 6 & 15 | (3 & j) << 4))], h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & k))]) : (h = h >>> 8 ^ c[255 & (h ^ (224 | j >> 12 & 15))], h = h >>> 8 ^ c[255 & (h ^ (128 | j >> 6 & 63))], h = h >>> 8 ^ c[255 & (h ^ (128 | 63 & j))])
     }
     return h ^ -1
     };
     return b(a) >>> 0
     }
     '''
        ctx = execjs.compile(js)
        return ctx.call('test', a)

class dyVideoDown2():
    def __init__(self):
        browser_name = 'chrome'
        executable_path = '/usr/local/bin/chromedriver'
        self.driver = Browser(driver_name=browser_name, executable_path=executable_path)
if __name__ == '__main__':
    dy_url = 'http://v.douyin.com/jTpfnb/'
    dy_down = dyVideoDown()
    dy_final_url = dy_down.get_video_url(dy_url=dy_url)
    if dy_final_url:
        dy_down.download(dy_final_url, '1.mp4', 'dy_mp4')
    else:
        print u'找不到链接'
