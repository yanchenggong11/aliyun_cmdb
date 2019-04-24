#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 15:28
# @Author  : yanfei

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
import re

class getBalance(object):
    def __init__(self,accessKeydatetimeID, accessSecret,regionID='cn-hangzhou'):
        self.accessKeydatetimeID = accessKeydatetimeID
        self.accessSecret = accessSecret
        self.regionID = regionID
        self.client = AcsClient(self.accessKeydatetimeID,self.accessSecret,self.regionID)
        self.request = CommonRequest()
        self.request.set_accept_format('json')
        self.request.set_domain('business.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_protocol_type('https')  # https | http
        self.request.set_version('2017-12-14')
        self.request.add_query_param('RegionId', self.regionID)

    def getbalance(self):
        self.request.set_action_name('QueryAccountBalance')
        try:
            respone = self.client.do_action_with_exception(self.request)
            account_info = json.loads(str(respone,encoding='utf-8'))
            account_balance = account_info["Data"]["AvailableAmount"]
            balance = float(account_balance.replace(',',''))
            return balance
        except Exception as e:
            print('获取账号余额失败!!!')




if __name__ == "__main__":
    aliyun = getBalance('LTAI2SphCHWFRXwX','bb8P8G8Q0gl27ZjtrlSTZhx6Zhps76').getbalance()
    print(aliyun)


