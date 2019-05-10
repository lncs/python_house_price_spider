# Author :  lncs
# Time:     2019-05-10 10:04
# File :    house_price_main.py
# Software: PyCharm
import lianjia_crawler as lianjia
import data_display as ds

# 填写需要爬取城市的列表(当前仅支持省会城市)
# USED_LIST = ['成都', '杭州', '重庆', '北京', '上海', '长沙', '西安', '兰州', ]
USED_LIST = ['重庆']


def main():
    # 获取链家网二手房房价信息保存到data文件夹中
    # lianjia.start(USED_LIST)

    # 将data文件夹中的数据进行分析，分析结果也图片形式保存在result文件夹中
    ds.show_figure()


if __name__ == '__main__':
    main()
