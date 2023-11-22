# -*- coding: UTF-8 -*-
# @Time : 2023/11/21 16:05 
# @Author : 刘洪波
import jieba
import time
import requests
from bigtools import headers, stopwords
from lxml import etree
import html2text
h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True


def count_keywords_from_paragraph_text(title: str, paragraph_texts: list):
    title_l = jieba.cut(title)
    title_l = [i.strip() for i in title_l]
    print(title_l)
    key_words = []
    for i in title_l:
        if i not in stopwords:
            key_words.append(i)
    print(key_words)
    max_num = 0
    max_text = None
    for p in paragraph_texts:
        count_num = 0
        for k in key_words:
            count_num += p.count(k)
        if count_num > max_num:
            max_text = p
            max_num = count_num
    return max_num, max_text


def get_text_from_p_tag(html_etree):
    text_from_p_tag = {}
    p_tag = html_etree.xpath('//body//p')
    for p in p_tag:
        p_html = etree.tostring(p, pretty_print=True, encoding='unicode')
        p_text = h.handle(p_html)
        p_text = p_text.strip()
        if '。' in p_text and len(p_text) > 2:
            text_from_p_tag[p_text] = p
    return text_from_p_tag


def get_text_from_main_body(html_text: str):
    main_body = None
    html_etree = etree.HTML(html_text)
    article_tag = html_etree.xpath('//article')
    h1_all_attr = [f'contains("{i}", "title")' for i in html_etree.xpath('//h1/@*')]
    title = []
    if h1_all_attr:
        title = html_etree.xpath(f'//h1[{" or ".join(h1_all_attr)}]//text()')
        title = [i.strip() for i in title]
    if not title:
        title = html_etree.xpath('//title//text()')
        title_meta = html_etree.xpath('//meta[contains("property", "title")]/@content')
        title += title_meta
        title = [i.strip() for i in title]
    title = title[0]
    if article_tag:
        if len(article_tag) > 1:
            main_body = article_tag[0].xpath('./..')[0]
        else:
            main_body = article_tag[0]
    else:
        text_from_p_tag = get_text_from_p_tag(html_etree)
        if text_from_p_tag:
            if title in text_from_p_tag:
                del text_from_p_tag[title]
            print(text_from_p_tag)
            max_num, max_text = count_keywords_from_paragraph_text(title, list(text_from_p_tag.keys()))
            if max_num and max_text:
                center_p = text_from_p_tag[max_text]
                print(max_num, max_text, center_p)
                main_body = center_p.xpath('./..')[0]

    if main_body is not None:
        selected_html = etree.tostring(main_body, pretty_print=True, encoding='unicode')
        print(selected_html)
        return h.handle(selected_html)
    return ''


def sing_st(url):
    print(url)

    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    print(resp.status_code)
    start_time = time.time()
    result = get_text_from_main_body(resp.text)
    print('\n\n\n****result****\n\n\n')
    print([result])

    print(time.time() - start_time)
    print('\n\n\n********\n\n\n')
    time.sleep(5)
