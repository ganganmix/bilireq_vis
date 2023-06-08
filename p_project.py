import time
from typing import Literal, Optional
import pandas
import numpy
from matplotlib import pyplot
from log import logger
import wordcloud
from wordcloud import STOPWORDS
import jieba
import cv2


title = int(time.time())

class Data:
    mid: list[int]
    name: list[str]
    sex: list[Literal['女', '男', '保密']]
    sign: list[Optional[str]]
    viptype: list[str]
    birthday: list[Optional[str]]

    def __str__(self):
        return f"mid:{self.mid}, name:{self.name}, sex:{self.sex}, sign:{self.sign}, viptype:{self.viptype}, birthday:{self.birthday}"
"""
数据类
mid 用户mid
name 用户名
sex 性别
sign 签名
viptype vip类型
birthday 生日
"""


def add_excel(data: Data):
    df_new = pandas.DataFrame({
        "mid": data.mid,
        "name": data.name,
        "sex": data.sex,
        "sing": data.sign,
        "viptype": data.viptype,
        "birthday": data.birthday
    })
    df_new.to_excel(f'{title}.xlsx', index=False)
    logger.info(df_new)
    return
"""
创建加入excel表的函数
"""
def pie(data1:list[str], data2:list[int], topic:str):
    X = numpy.array(data2)
    pyplot.figure(figsize=(6, 4,))
    pyplot.pie(X, labels=data1, autopct='%1.2f%%', pctdistance=0.8)
    pyplot.rcParams['font.sans-serif'] = ['SimHei']
    pyplot.rcParams['axes.unicode_minus'] = False
    pyplot.title(topic)
    pyplot.savefig(f"{topic}.png", dpi=300)
    logger.info('图片生成成功')
    return
"""
饼状图画
"""


def keywordcloud(text: str, topic: str):
    keydata = ' '.join(jieba.cut(text))
    logger.info(keydata)
    backgroud = cv2.imread(r'OIP-C.jpg')
    myCloudword = wordcloud.WordCloud(font_path='simsun.ttc',
                                      width=400, height=200,
                                      mask=backgroud,
                                      scale=1,
                                      max_words=200,
                                      min_font_size=4,
                                      stopwords=STOPWORDS,
                                      random_state=50,
                                      background_color='white',
                                      max_font_size=100
                                      )
    myCloudword.generate(keydata)
    myCloudword.to_file(f"{topic}.jpg")
    logger.info(f"{topic}.png" + '图片生成成功')
    return

if __name__ == '__main__':
    data = Data()
        # data.mid = [1553, 45485, 51653]
    # data.name = ['banil', 'aonx ', 'cjac']
    # data.sign = ['cnalk', 'ansix', 'cailk']
    # data.viptype = ['ncaj', 'cnal', 'cjac']
    # data.birthday = ['ancl', 'cjaoss', 'coa']
    # data.sex = ['男', '女', '保密']
    # pie(data.sex, data.mid, '阿森纳承诺书')
