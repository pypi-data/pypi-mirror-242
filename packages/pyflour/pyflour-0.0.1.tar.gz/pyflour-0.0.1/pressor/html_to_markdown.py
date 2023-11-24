# -*- coding: UTF-8 -*-
# @Time : 2023/11/22 18:46 
# @Author : 刘洪波
import html2text

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True


def html_to_markdown(data):
    return h.handle(data)