# -*- coding: UTF-8 -*-
# @Time : 2023/11/22 11:41 
# @Author : 刘洪波

from parse_html import get_text_from_main_body


def html_parser(html_text):
    return get_text_from_main_body(html_text)


func_dict = {
    'html': html_parser
}


def file_parser(data, type):
    if type in func_dict:
        func = func_dict.get(type)
        return func(data)
    return []
