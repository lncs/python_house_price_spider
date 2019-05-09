# Author :  lncs
# Time:     2019-05-08 19:38
# File :    constant.py
# Software: PyCharm

import pinyin

# 全国各省市的xinxi
# ref: https://github.com/baixuexiyang/geocoord
_PROVINCE_INFO = [
    # 23省
    {'province': '甘肃', 'capital': '兰州', 'geoCoord': [103.73, 36.03], 'abbreviation': '甘/陇'},
    {'province': '青海', 'capital': '西宁', 'geoCoord': [101.74, 36.56], 'abbreviation': '青'},
    {'province': '四川', 'capital': '成都', 'geoCoord': [104.06, 30.67], 'abbreviation': '川/蜀'},
    {'province': '河北', 'capital': '石家庄', 'geoCoord': [114.48, 38.03], 'abbreviation': '冀'},
    {'province': '云南', 'capital': '拉萨', 'geoCoord': [102.73, 25.04], 'abbreviation': '云/滇'},
    {'province': '贵州', 'capital': '贵阳', 'geoCoord': [106.71, 26.57], 'abbreviation': '黔/贵'},
    {'province': '湖北', 'capital': '武汉', 'geoCoord': [114.31, 30.52], 'abbreviation': '鄂'},
    {'province': '河南', 'capital': '郑州', 'geoCoord': [113.65, 34.76], 'abbreviation': '豫'},
    {'province': '山东', 'capital': '济南', 'geoCoord': [117, 36.65], 'abbreviation': '鲁'},
    {'province': '江苏', 'capital': '南京', 'geoCoord': [118.78, 32.04], 'abbreviation': '苏'},
    {'province': '安徽', 'capital': '合肥', 'geoCoord': [117.27, 31.86], 'abbreviation': '皖'},
    {'province': '浙江', 'capital': '杭州', 'geoCoord': [120.19, 30.26], 'abbreviation': '浙'},
    {'province': '江西', 'capital': '南昌', 'geoCoord': [115.89, 28.68], 'abbreviation': '赣'},
    {'province': '福建', 'capital': '福州', 'geoCoord': [119.3, 26.08], 'abbreviation': '闽'},
    {'province': '广东', 'capital': '广州', 'geoCoord': [113.23, 23.16], 'abbreviation': '粤'},
    {'province': '湖南', 'capital': '长沙', 'geoCoord': [113, 28.21], 'abbreviation': '湘'},
    {'province': '海南', 'capital': '海口', 'geoCoord': [110.35, 20.02], 'abbreviation': '琼'},
    {'province': '辽宁', 'capital': '沈阳', 'geoCoord': [123.38, 41.8], 'abbreviation': '辽'},
    {'province': '吉林', 'capital': '长春', 'geoCoord': [125.35, 43.88], 'abbreviation': '吉'},
    {'province': '黑龙江', 'capital': '哈尔滨', 'geoCoord': [126.63, 45.75], 'abbreviation': '黑'},
    {'province': '山西', 'capital': '太原', 'geoCoord': [112.53, 37.87], 'abbreviation': '晋'},
    {'province': '陕西', 'capital': '西安', 'geoCoord': [108.95, 34.27], 'abbreviation': '陕/秦'},
    {'province': '台湾', 'capital': '台北', 'geoCoord': [121.30, 25.03], 'abbreviation': '台'},
    # 4直辖市
    {'province': '北京', 'capital': '北京', 'geoCoord': [116.46, 39.92], 'abbreviation': '京'},
    {'province': '上海', 'capital': '上海', 'geoCoord': [121.48, 31.22], 'abbreviation': '沪'},
    {'province': '重庆', 'capital': '重庆', 'geoCoord': [106.54, 29.59], 'abbreviation': '渝'},
    {'province': '天津', 'capital': '天津', 'geoCoord': [117.2, 39.13], 'abbreviation': '津'},
    # 5自治区
    {'province': '内蒙古', 'capital': '呼和浩特', 'geoCoord': [111.65, 40.82], 'abbreviation': '内蒙古'},
    {'province': '广西', 'capital': '南宁', 'geoCoord': [108.33, 22.84], 'abbreviation': '桂'},
    {'province': '西藏', 'capital': '拉萨', 'geoCoord': [91.11, 29.97], 'abbreviation': '藏'},
    {'province': '宁夏', 'capital': '银川', 'geoCoord': [106.27, 38.47], 'abbreviation': '宁'},
    {'province': '新疆', 'capital': '乌鲁木齐', 'geoCoord': [87.68, 43.77], 'abbreviation': '新'},
    # 2特别行政区
    {'province': '香港', 'capital': '香港', 'geoCoord': [114.17, 22.28], 'abbreviation': '港'},
    {'province': '澳门', 'capital': '澳门', 'geoCoord': [113.54, 22.19], 'abbreviation': '澳'}
]


PROVINCE_INFO = [
    {'capital': item['capital'],
     'cpinyin': pinyin.get(item['capital'], format="strip", delimiter=""),
     'cshortpinyin': pinyin.get_initial(item['capital'], delimiter=""),
     'coord': item['geoCoord']
     } for item in _PROVINCE_INFO
]

def get_all_info():
    all_info = []
    for city in PROVINCE_INFO:
        # print(city)
        all_info.append(city)
    return all_info

def get_info(in_param):
    result_info = []
    for all_info in PROVINCE_INFO:
        for k, v in all_info.items():
            # print(k)
            if v in in_param:
                # print(all_info.items())
                if v == "重庆":
                    tmp = {
                        'capital': all_info.get('capital'),
                        'cpinyin': 'chongqing',
                        'cshortpinyin': 'cq',
                        'coord': all_info.get('coord'),
                    }
                else:
                    tmp = {
                        'capital': all_info.get('capital'),
                        'cpinyin': all_info.get('cpinyin'),
                        'cshortpinyin': all_info.get('cshortpinyin'),
                        'coord': all_info.get('coord'),
                    }
                result_info.append(tmp)
    return result_info

if __name__ == '__main__':

    USED_LIST = [
        '成都',
        '杭州',
        '重庆',
        '北京',
        '上海',
        '长沙',
        '西安',
        '兰州',
    ]
    print(get_info(USED_LIST))