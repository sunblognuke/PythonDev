#!/usr/bin/env python
# coding: utf-8

import os, sys, re

reload(sys)
sys.setdefaultencoding('utf-8')

def replace_charentity(html):
    """
    ##替换常用HTML字符实体.
    #使用正常的字符替换HTML中特殊的字符实体.
    #你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
    #@param htmlstr HTML字符串.
    """
    char_entities = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charentity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charentity.search(html)
    while sz:
        entity = sz.group()  # entity全称，如&gt;
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            html = re_charentity.sub(char_entities[key], html, 1)
            sz = re_charentity.search(html)
        except KeyError:
            # 以空串代替
            html = re_charentity.sub('', html, 1)
            sz = re_charentity.search(html)
    return html
