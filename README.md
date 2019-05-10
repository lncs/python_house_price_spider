# 项目简介
> 爬取链家网二手房信息  
# 使用方法
> 安装依赖
```
pip install -r requirements.txt
```
> 填写需要爬取的城市列表到 house_price_main.py 中的 USED_LIST  
> 执行程序，获取房价数据存放在data文件夹中，并生产分析图片存放在result文件夹中
```
python house_price_main.py
```
### 其他
> constant.py 文件中是中国各省省会的经纬度、简称等信息，并且提供了由中文名称获取对应拼音全写和简写的方法，方便url拼接