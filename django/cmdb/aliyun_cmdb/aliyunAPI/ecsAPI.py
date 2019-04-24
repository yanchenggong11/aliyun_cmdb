#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 15:40
# @Author  : yanfei

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceStatusRequest import DescribeInstanceStatusRequest
from aliyunsdkecs.request.v20140526.StartInstanceRequest import StartInstanceRequest
from aliyunsdkecs.request.v20140526.StopInstanceRequest import StopInstanceRequest
from aliyunsdkecs.request.v20140526.ModifyInstanceAttributeRequest import ModifyInstanceAttributeRequest
import json


class EcsOperating(object):
    def __init__(self,accessKeyId,accessSecret, regionID='cn-hangzhou'):
        self.__accessKeyId = accessKeyId
        self.__accessSecret =accessSecret
        self.__regionId = regionID
        self.__client = AcsClient(self.__accessKeyId,self.__accessSecret,self.__regionId)

    def get_ecs_status(self):
        '''
        获取ecs列表，及ecs相关状态信息
        :return: ecs状态信息列表
        '''
        ecs_list = []
        request = DescribeInstancesRequest()
        request.set_accept_format('json')
        try:
            response = self.__client.do_action_with_exception(request)
            ecs_info = json.loads(response,encoding='utf-8')['Instances']['Instance']
            if ecs_info:
                for ecs in ecs_info:
                    ecs_dict = {}
                    ecs_dict["InstanceId"] = ecs["InstanceId"]
                    ecs_dict["InstanceName"] = ecs["InstanceName"]
                    ecs_dict["Cpu"] = ecs["Cpu"]
                    ecs_dict["Memory"] = ecs["Memory"]
                    pubIp_list = ecs["PublicIpAddress"]["IpAddress"]
                    if pubIp_list:
                        ecs_dict["PubIp"] = pubIp_list[0]
                    else:
                        ecs_dict["PubIp"] = None
                    ecs_dict["PivIp"] = ecs["NetworkInterfaces"]["NetworkInterface"][0]["PrimaryIpAddress"]
                    ecs_dict["Status"] = ecs["Status"]
                    ecs_dict["ExpiredTime"] = ecs["ExpiredTime"]
                    ecs_list.append(ecs_dict)

            else:
                print('主机列表为空!!!!')
            return ecs_list
        except Exception as e:
            print(e)
            print('获取主机状态列表失败')

    def check_ecs_status(self,InstanceId):
        request = DescribeInstanceStatusRequest()
        request.set_accept_format('json')
        try:
            response = self.__client.do_action_with_exception(request)
            instance_status = json.loads(response,encoding='utf-8')['InstanceStatuses']["InstanceStatus"]
            if instance_status:
                for ecs in instance_status:
                    if ecs['InstanceId'] == InstanceId:
                        ecs_status = ecs['Status']
                        print(ecs['InstanceId'],ecs_status)
            else:
                print('%s 实例状态获取失败！！！' % InstanceId)

            if ecs_status == 'Running':
                return True
            else:
                return False
        except Exception as e:
            print(e)
            print('%s 实例状态获取失败！！！' % InstanceId)

    def start_instance(self,InstanceId):
        request = StartInstanceRequest()
        request.set_accept_format('json')
        request.set_InstanceId(InstanceId)
        status = self.check_ecs_status(InstanceId)
        if not status:
            try:
                response = self.__client.do_action_with_exception(request)
            except Exception as e:
                print(e)
                print('%s 实例启动失败' % InstanceId)
        else:
            print('%s 实例状态不为Stopping，无法启动!!!!' %InstanceId)

    def stop_instance(self,InstanceId):
        request = StopInstanceRequest()
        request.set_accept_format('json')
        request.set_InstanceId(InstanceId)

        status = self.check_ecs_status(InstanceId)
        if status:
            try:
                response = self.__client.do_action_with_exception(request)
                print('%s 实例已关闭' % InstanceId)
            except Exception as e:
                print(e)
                print('%s 实例关闭失败！！！' % InstanceId)
        else:
            print('%s 实例状态不为Running,无法关闭!!!!' % InstanceId)

    def reset_password(self,InstanceId,passwd):
        request = ModifyInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_Password(passwd)
        request.set_InstanceId(InstanceId)
        try:
            response = self.__client.do_action_with_exception(request)
        except Exception as e:
            print(e)
            print('%s 实例获取阿里云数据失败!!!!' % InstanceId)


if __name__ == '__main__':
    ecsobj = EcsOperating('LTAIWyc9JgUOjI8V','KhFzBAxWJKG8Wh849UwM3eZyi0UglO')
    # ecsobj.stop_instance('i-bp17awwjkah1lxj7h9tp')
    # print(ecsobj.get_ecs_status())

    # print(ecsobj.start_instance('i-bp17awwjkah1lxj7h9tp'))
    #
    #
    # print(ecsobj.check_ecs_status('i-bp17awwjkah1lxj7h9tp'))

