# Author :  lncs
# Time:     2019-05-09 14:43
# File :    data_display.py
# Software: PyCharm
import json
import matplotlib.pyplot as plt
import matplotlib
import os
from logpublic import *

# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
# matplotlib.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def load_data(filename):
    '''
    从data文件夹下加载json文件
    :param filename:
    :return:
    '''
    data = None
    with open(filename, 'r', encoding='utf8') as f:
        line = f.read()
        data = json.loads(line)

    data_dic = {}
    for i in range(len(data)):
        # 已下架房源中价格为空，不计入分析数据
        if "" != data[i].get('price'):
            price = (int)(data[i].get('price'))
            area = data[i].get('area')
            try:
                data_dic[area].append(price)
            except:
                data_dic[area] = [price]
    app_logger.debug('{}数据:{}'.format(filename, data_dic))
    return data_dic


def split_data(data_dic):
    area_data = {}
    for area in data_dic.keys():
        area_data[area] = {'max': data_dic[area][0], 'min': data_dic[area][0], 'average': 0, 'count': 0}
        for price in data_dic[area]:
            if price > area_data[area]['max']:
                area_data[area]['max'] = price
            if price < area_data[area]['min']:
                area_data[area]['min'] = price
            area_data[area]['average'] += price
        area_data[area]['average'] /= len(data_dic[area])
        # 保留两位小数
        area_data[area]['average'] = round(area_data[area]['average'])
        area_data[area]['count'] = len(data_dic[area])
    return area_data


def display_data(file_name, data_dic):
    max = []
    min = []
    average = []
    label_list = data_dic.keys()
    sorted_list = sorted(list(label_list))
    for label in sorted_list:
        max.append(data_dic[label].get('max'))
        min.append(data_dic[label].get('min'))
        average.append(data_dic[label].get('average'))
    x = range(len(max))
    """
    绘制条形图
    left：柱图中点横坐标
    height：高度
    width：宽度，默认0.8
    label：
    """
    plt.figure(figsize=(13.66, 7.68))
    rects1 = plt.bar(x=x, height=max, width=0.25, alpha=0.8, color='red', label="最大值")
    rects2 = plt.bar(x=[i + 0.25 for i in x], height=average, width=0.25, color='green', label="平均值")
    rects3 = plt.bar(x=[i + 0.5 for i in x], height=min, width=0.25, color='blue', label="最小值")
    # plt.ylim(0, 50) # y轴取值范围
    plt.ylabel("房价/元")
    """
    设置x轴刻度显示值
    参数一：中点坐标
    参数二：显示值
    """
    plt.xticks([index + 0.25 for index in x], sorted_list)
    plt.xlabel("区域")
    title = "{}二手房价格分析图".format(file_name)
    plt.title(title)
    # plt.legend(loc=1)  # 设置题注 # 编辑文本
    plt.legend()
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    for rect in rects2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    for rect in rects3:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")

    # plt.show()
    if not os.path.exists("./result/"):
        os.mkdir("./result/")
    plt.savefig('./result/' + title + '.png')


def show_house_count(file_name, data_dic):
    count = []
    area = []
    label_list = data_dic.keys()
    sorted_list = sorted(list(label_list))
    for label in sorted_list:
        count.append(data_dic[label].get('count'))
        area.append(label)

    for i in range(len(data_dic)):
        app_logger.info('{}-{}房屋套数:{}'.format(file_name, area[i], count[i]))
    app_logger.info('{}-房屋总套数:{}'.format(file_name, sum(count)))


def show_figure():
    file_list = os.listdir("./data")
    for i in range(len(file_list)):
        path = os.path.join('./data/' + file_list[i])
        file_name = os.path.splitext(file_list[i])[0]
        app_logger.debug('当前读取文件:{}'.format(path))

        data_dic = load_data(path)
        area_data = split_data(data_dic)
        display_data(file_name, area_data)
        show_house_count(file_name, area_data)


if __name__ == '__main__':
    # data_dic = load_data('data/杭州(2019-09-23).json')
    # print(type(data_dic))
    # area_data = split_data(data_dic)
    # print(area_data)
    # display_data('测试', area_data)
    # # print(area_data)
    show_figure()
