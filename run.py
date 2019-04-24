#!/usr/bin/python
# -*- coding: utf-8 -*-

from Douyin.dyVideoDown import DyVideoDown

from WebPractice.server import Server


if __name__ == '__main__':
    # dy_url = 'http://v.douyin.com/jTpfnb/'
    # dy_down = DyVideoDown()
    # dy_final_url = dy_down.get_video_url(dy_url=dy_url)
    # if dy_final_url:
    #     dy_down.download(dy_final_url, '1.mp4', 'dy_mp4')
    # else:
    #     print u'找不到链接'
    s = Server()