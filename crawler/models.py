# -*- coding: utf-8 -*-

from django.db import models
from bs4 import BeautifulSoup
import requests
# Create your models here.

base_url = 'http://www.chinalawnews.cn/'


def crawler_news():
    r = requests.get(base_url)
    html_doc = r.content
    return BeautifulSoup(html_doc)


def find_banner_node(banner):
    datas = []
    for node in banner:
        links = node.find_all('a')
        for a in links:
            if a.img is not None:
                title = a['title']
                href = base_url + a['href']
                img_alt = a.img['alt']
                img_src = base_url + a.img['src']
                data = {
                    'title': title,
                    'href': href,
                    'img_alt': img_alt,
                    'img_src': img_src
                }
                datas.append(data)
    return datas
