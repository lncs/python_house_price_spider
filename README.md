# 项目简介
> 爬取链家网二手房信息  
# 使用方法
> 安装依赖
```
pip install -r requirements.txt
```
> 填写需要爬取的城市列表到 lianjia_crawler.py 中的 USED_LIST  
> 执行数据爬取, 所得数据在 data 文件夹中
```
python lianjia_crawler.py
```
> 执行数据分析,生成内容存放在 result 文件夹中
```
python data_display.py
```
### 其他
> constant.py 文件中是中国各省省会的经纬度、简称等信息，并且提供了由中文名称获取对应拼音全写和简写的方法，方便url拼接