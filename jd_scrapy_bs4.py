#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import urllib.request
from bs4 import BeautifulSoup
import os
from datetime import datetime
from ProgressBar import ProgressBar

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0")
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response, 'lxml')
    return soup


def bytes_url_open(url):
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0")
    response = urllib.request.urlopen(req)
    html = response.read()
    return html


def get_page(url, page_num):
    start = url_open(url).find(
        'span', {'class': 'current-comment-page'}).get_text()
    start_num = int(start[1:-1])
    download_page = []
    for i in range(page_num):
        download_page.append(start_num - i)
    download_list = []
    for j in download_page:
        download_list.append(
            'http://jandan.net/ooxx/page-' + str(j) + '#comments')
    return download_list


def find_imgs(page_url):
    html = url_open(page_url).findAll('a', {'class': 'view_img_link'})
    img_addrs = []
    for i in html:
        img_addrs.append('http:' + i['href'])
    return img_addrs


def save_imgs(img_addrs):
    bar = ProgressBar(max_value=len(img_addrs), name="download_imgs")
    bar.start()
    for each in img_addrs:
        filename = each.split('/')[-1]
        with open(filename, 'wb') as f:
            img = bytes_url_open(each)
            f.write(img)
            bar.update()

def jddowngrils(pages=2):
    realpath = None
    path = 'D:\\python test\\urllearning\\'
    os.chdir(path)
    folder = 'OOXX_' + datetime.now().strftime('%Y%m%d')
    realpath = os.getcwd() + '\\' + folder
    if not os.path.exists(realpath):
        os.mkdir(folder)
    os.chdir(folder)

    url = 'http://jandan.net/ooxx/'
    page_list = get_page(url, pages)

    for i in page_list:
        img_addrs = find_imgs(i)
        save_imgs(img_addrs)
    print('Done')

if __name__ == '__main__':
    jddowngrils()
