# Author :  lncs
# Time:     2019-05-08 19:33
# File :    lianjia_crawler.py
# Software: PyCharm

import requests
from pyquery import PyQuery as pq
from concurrent.futures import ThreadPoolExecutor
import json
import constant
import os
import time
from logpublic import *


def save_data(data, filename):
    if not os.path.exists("./data/"):
        os.mkdir("./data/")
    dest_name = "./data/" + filename + '(' + time.strftime("%Y-%m-%d") + ").json"
    with open(dest_name, 'w', encoding="utf8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))


# 需要先在本地开启代理池
# 代理池仓库: https://github.com/Python3WebSpider/ProxyPool
def get_valid_ip():
    url = "http://127.0.0.1:6379/get"
    try:
        ip = requests.get(url).text
        return ip
    except Exception as e:
        print("请先运行代理池", e)


def get_page_url_list(start_url):
    # print(start_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    try:
        response = requests.get(start_url, headers=headers)
        # print(response.status_code, response.text)
        doc = pq(response.text)
        total_num = int(doc(".resultDes .total span").text())
        total_page = total_num // 30 + 1
        # print('总套数：{}，总页数：{}'.format(total_num, total_page))
        location = start_url.split('/')[2].split('.')[0]
        app_logger.info('{}-二手房总套数:{}'.format(constant.get_name_from_pinyin(location), total_num))

        # 只能访问到前一百页
        if total_page > 100:
            total_page = 100

        page_url_list = list()

        for i in range(total_page):
            url = start_url + "/pg" + str(i + 1) + "/"
            page_url_list.append(url)
            # print(url)
        return page_url_list
    except Exception as e:
        app_logger.error('获取总套数出错,请确认起始URL是否正确:{}'.format(start_url), e)
        return None


def get_page_url_list_filter(start_url, filter_args):
    '''
    根据起始url开始获取数据，可以具体到某一城市的区域(拼音全拼)、售价(p)、房型(l)、面积(a)、标签(拼音简写)等
    示例：https://cd.lianjia.com/ershoufang/wuhou/pg3l2l3/
    :param start_url: 起始url
    :param filter_args: 过滤参数
    :return:
    '''
    start_url = start_url + '/' + filter_args
    app_logger.info('入口url:{}'.format(start_url))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    try:
        response = requests.get(start_url, headers=headers)
        # print(response.status_code, response.text)
        doc = pq(response.text)
        total_num = int(doc(".resultDes .total span").text())
        total_page = total_num // 30 + 1
        # print('总套数：{}，总页数：{}'.format(total_num, total_page))
        location = start_url.split('/')[2].split('.')[0]
        app_logger.info('{}-当前筛选条件下房屋总套数:{}'.format(constant.get_name_from_pinyin(location), total_num))

        # 只能访问到前一百页
        if total_page > 100:
            total_page = 100

        page_url_list = list()

        for i in range(total_page):
            url = start_url + "/pg" + str(i + 1) + filter_args + "/"
            page_url_list.append(url)
            # print(url)
        return page_url_list
    except Exception as e:
        app_logger.error('获取总套数出错,请确认起始URL是否正确:{}'.format(start_url), e)
        # print("获取总套数出错,请确认起始URL是否正确")
        return None


detail_list = list()


def get_detail_page_url(page_url):
    global detail_list
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer': 'https://bj.lianjia.com/ershoufang'
    }

    try:
        response = requests.get(page_url, headers=headers, timeout=3)
        doc = pq(response.text)
        # broswer.get(page_url)
        # print(page_url)
        # doc = pq(broswer.page_source)
        i = 0
        detail_urls = list()
        for item in doc(".sellListContent li").items():
            i += 1
            if i == 31:
                break
            child_item = item(".noresultRecommend")
            if child_item == None:
                i -= 1
            detail_url = child_item.attr("href")
            detail_urls.append(detail_url)
        return detail_urls
    except Exception as e:
        print("获取列表页" + page_url + "出错", e)


def parser_detail_page(res):
    global detail_list
    detail_urls = res.result()
    if not detail_urls:
        print("detail url 为空")
        return None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer': 'https://bj.lianjia.com/ershoufang'
    }
    for detail_url in detail_urls:
        try:
            response = requests.get(url=detail_url, headers=headers, timeout=3)
            # print(response.status_code)
            detail_dict = dict()
            doc = pq(response.text)
            unit_price = doc(".unitPriceValue").text()
            unit_price = unit_price[0:unit_price.index("元")]
            title = doc("h1").text()
            area = doc(".areaName .info a").eq(0).text().strip()
            url = detail_url
            detail_dict["title"] = title
            detail_dict["area"] = area
            detail_dict["price"] = unit_price
            detail_dict["url"] = url

            detail_list.append(detail_dict)

            print(unit_price, title, area)

        except Exception as e:
            print("获取详情页出错,换ip重试", e)
            proxies = {
                "http": "http://" + get_valid_ip(),
            }
            try:
                response = requests.get(url=detail_url, headers=headers, proxies=proxies)
                # print(response.status_code)
                detail_dict = dict()
                doc = pq(response.text)
                unit_price = doc(".unitPriceValue").text()
                unit_price = unit_price[0:unit_price.index("元")]
                title = doc("h1").text()
                area = doc(".areaName .info a").eq(0).text().strip()
                url = detail_url
                # 已下架的还会爬取，但是没有价格
                if len(unit_price) > 0:
                    detail_dict["title"] = title
                    detail_dict["area"] = area
                    detail_dict["price"] = unit_price
                    detail_dict["url"] = url

                    detail_list.append(detail_dict)

                    print(unit_price, title, area)
            except Exception as e:
                print("重试失败...", e)


def start(city_list):
    city_list = constant.get_info(city_list)
    print(city_list)
    for city_dic in city_list:
        # 获得二手房信息的起始页url
        start_url = "https://{}.lianjia.com/ershoufang".format(city_dic['cshortpinyin'])
        app_logger.info('起始url:{}'.format(start_url))
        page_url_list = get_page_url_list(start_url)
        app_logger.info('url列表:{}'.format(page_url_list))
        # print(page_url_list)
        with ThreadPoolExecutor(30) as executor:
            for page_url in page_url_list:
                executor.submit(get_detail_page_url, page_url).add_done_callback(parser_detail_page)

        save_data(detail_list, city_dic['capital'])
        detail_list.clear()


def start_detail_args(filename, start_url, filter_args):
    '''
    根据起始url开始获取数据，可以具体到某一城市的区域(拼音全拼)、售价(p)、房型(l)、面积(a)、标签(拼音简写)等
    :param filename:数据保存的文件名
    :param start_url:起始url
    :param filter_args:筛选参数
    :return:
    '''
    page_url_list = get_page_url_list_filter(start_url, filter_args)
    app_logger.info('url列表:{}'.format(page_url_list))
    # print(page_url_list)
    with ThreadPoolExecutor(30) as executor:
        for page_url in page_url_list:
            executor.submit(get_detail_page_url, page_url).add_done_callback(parser_detail_page)

    save_data(detail_list, filename)
    detail_list.clear()


if __name__ == '__main__':
    USED_LIST = ['成都']
    start(USED_LIST)
    start_detail_args('成都-武侯', 'https://cd.lianjia.com/ershoufang/wuhou', 'l2l3p2')
