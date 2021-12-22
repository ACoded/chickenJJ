#!/usr/bin/env python
# coding=utf-8

import json
import urllib2

VALUATION = "https://danjuanapp.com/djapi/fund/estimate-nav/%s"
FUNDINSO = 'https://danjuanapp.com/djapi/fund/%s'
FUND_LIST = [
    ("004753", 8757.4),
    ("012805", 4198.8),
    ("501048", 1720.47),
    ("470018", 497.86),
    ("167301", 6948.04),
    ("000136", 1899.16),
    ("000294", 1722.01),
    ("009076", 4781.16),
    ("005734", 460.07),
    ("008087", 10004.56),
    ("006381", 3902.72),
    ("163417", 3418.79),
    ("519772", 2803.99),
    ("006253", 25.46),
    ("011609", 847.82),
    ("100060", 2119.56),
    ("002079", 1666.82),
    ("000452", 110.06),
]


def get(url):
    # 模拟浏览器用户标识
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    req = urllib2.Request(url=url, headers=headers)
    return urllib2.urlopen(req).read()


def beauty_print(data):
    if data[1] > 0:
        print('%s\t| +%.2f%%' % data)
    else:
        print('%s\t| %.2f%%' % data)


valuation_url = VALUATION
fund_info = FUNDINSO
total_count = 0
total_va = 0

print '基金名称 \t\t', '增长率\t', '金额'

for fund in FUND_LIST:
    res = json.loads(get(valuation_url % (fund[0])))
    info = json.loads(get(fund_info % (fund[0])))
    mv = float(info['data']['fund_derived']['unit_nav']) * fund[1]
    total_count += mv

    if res['result_code'] == 600001:
        print fund[1], res['message']
        break
    if len(res['data']['items']) == 0:
        print info['data']['fd_name'], '暂无更新'
    elif len(res['data']['items']) > 0:
        percent = res['data']['items'][-1]['percentage']
        va = percent * mv / 100
        total_count += va
        total_va += va
        print info['data']['fd_name'], '%.2f%%' % (percent), '\t', va
print total_count, '今日预计总收益', total_va
