import random
from log import logger
from b_project import get_biliuserinfo
from p_project import pie, add_excel, keywordcloud, Data

def bili_data(size:int):
    mid_list = []
    for i in range(size):
        data = Data()
        rec = get_biliuserinfo(random.randint(0, 5400000)).get().json().get('data')
        if rec:
            try:
                data.mid = rec.get('mid')
                data.name = rec.get('name')
                data.sex = rec.get('sex')
                data.sign = rec.get('sign')
                data.viptype = rec.get('vip').get('label').get('text')
                data.birthday = rec.get('birthday')
                logger.info(data.__str__())
                mid_list.append(data)
            except AttributeError:
                raise '网络问题，请重试'
    return mid_list


if __name__ == '__main__':
    midl = []
    namel = []
    sexl = []
    signl = []
    viptypel = []
    birthdayl = []
    wvip = [0, 0]
    vip = ['年度大会员', '非年度大会员']
    sl = ['男', '女', '保密']
    sld = [0, 0, 0]
    try:
        i = int(input('爬取多少'))
    except TypeError:
        raise '输入类型错误'
    datalist = bili_data(i)
    kw1 = ''
    kw2 = ''
    sl = ['男', '女', '保密']
    sld = [0, 0, 0]
    for i in datalist:
        midl.append(i.mid)
        namel.append(i.name)
        sexl.append(i.sex)
        signl.append(i.sign)
        viptypel.append(i.viptype)
        birthdayl.append(i.birthday)
        if i.name:
            kw1 += i.name
        if i.sign:
            kw2 += kw2
        if i .sex:
            if i.sex == '男':
                sld[0] = sld[0] + 1
            if i.sex == '女':
                sld[1] = sld[1] + 1
            if i.sex == '保密':
                sld[2] = sld[2] + 1
                # 男女圆饼图
        if not i.viptype:
            wvip[1] = wvip[1] + 1
        if i.viptype:
            wvip[0] = wvip[0] + 1
        # 会员饼状图
    pie(data1=vip, data2=wvip, topic="会员饼状图")
    pie(data1=sl, data2=sld, topic="男女圆饼图")
    d = Data()
    d.name = namel
    d.sign = signl
    d.sex = sexl
    d.viptype = viptypel
    d.mid = midl
    d.birthday = birthdayl
    add_excel(d)
    keywordcloud(kw1, topic='name词云')
    logger.warning(kw1)
    if kw2:
        keywordcloud(kw2, topic='sign饼图')
        logger.warning(kw2)