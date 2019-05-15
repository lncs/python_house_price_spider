# Author :  lncs
# Time:     2019-05-10 11:03
# File :    request_test.py
# Software: PyCharm

import requests
from pyquery import PyQuery as pq


def main():
    start_url = "https://hz.lianjia.com/ershoufang"
    # print(start_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }

    # 1、页url
    r = requests.get(start_url, headers=headers)
    # print(r.content)
    # print(r.headers)

    doc = pq(r.text)
    # print(doc)
    total_num = int(doc(".resultDes .total span").text())
    # print(total_num)

    # print(r.text)

    # 2、详情url
    detail_url_info = "https://hz.lianjia.com/ershoufang/pg1/"
    r = requests.get(start_url, headers=headers)
    doc = pq(r.text)
    i = 0
    for item in doc(".sellListContent li").items():
        i += 1
        if i == 31:
            break
        child_item = item(".noresultRecommend")
        if child_item == None:
            i -= 1
        detail_url = child_item.attr("href")
        print(detail_url)

    # 3、详情页数据分析

    detail_url = "https://hz.lianjia.com/ershoufang/103104518638.html"
    response = requests.get(url=detail_url, headers=headers, timeout=3)
    # print(response.status_code)
    detail_dict = dict()
    doc = pq(response.text)
    print(doc)
    unit_price = doc(".unitPriceValue").text()
    unit_price = unit_price[0:unit_price.index("元")]
    title = doc("h1").text()
    area = doc(".areaName .info a").eq(0).text().strip()
    url = detail_url
    detail_dict["title"] = title
    detail_dict["area"] = area
    detail_dict["price"] = unit_price
    detail_dict["url"] = url

    print(unit_price, title, area)


if __name__ == '__main__':
    main()
