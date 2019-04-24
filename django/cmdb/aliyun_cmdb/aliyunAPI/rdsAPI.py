#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 14:33
# @Author  : yanfei

# DESC: operating aliyun RDS

from aliyunsdkcore.client import AcsClient
from aliyunsdkrds.request.v20140815.DescribeDBInstancesRequest import DescribeDBInstancesRequest
from aliyunsdkrds.request.v20140815.CreateDatabaseRequest import CreateDatabaseRequest
from aliyunsdkrds.request.v20140815.DescribeAccountsRequest import DescribeAccountsRequest
from aliyunsdkrds.request.v20140815.CreateAccountRequest import CreateAccountRequest
from aliyunsdkrds.request.v20140815.GrantAccountPrivilegeRequest import GrantAccountPrivilegeRequest
from aliyunsdkrds.request.v20140815.RevokeAccountPrivilegeRequest import RevokeAccountPrivilegeRequest
from aliyunsdkrds.request.v20140815.ResetAccountPasswordRequest import ResetAccountPasswordRequest
from aliyunsdkrds.request.v20140815.DeleteAccountRequest import DeleteAccountRequest
from aliyunsdkrds.request.v20140815.DescribeDBInstanceAttributeRequest import DescribeDBInstanceAttributeRequest
from aliyunsdkrds.request.v20140815.DescribeDatabasesRequest import DescribeDatabasesRequest
import json
import datetime


class checkZoneRdsID(object):
    def __init__(self, accessKeyID, accessSecret, regionID='cn-hangzhou'):
        self._accessKeyID = accessKeyID
        self._accessSecret = accessSecret
        self._regionID = regionID
        self._client = AcsClient(self._accessKeyID, self._accessSecret, self._regionID)

    def get_rds_id(self,p_name):
        request = DescribeDBInstancesRequest()
        request.set_accept_format('json')
        try:
            response = self._client.do_action_with_exception(request)
            info = json.loads(str(response, encoding='utf-8'))
            db_instance = info["Items"]["DBInstance"]
            for instance in db_instance:
                if p_name == instance["DBInstanceDescription"]:
                    rds_instance = instance["DBInstanceId"]
            return rds_instance
        except:
            print('%s 获取RDS实例失败!!!!' % p_name)



class operatingRds(object):
    def __init__(self,accessKeyID, accessSecret,DBInstanceId,regionID='cn-hangzhou'):
        self._accessKeyID = accessKeyID
        self._accessSecret = accessSecret
        self._regionID = regionID
        self._DBInstanceId = DBInstanceId
        self._client = AcsClient(self._accessKeyID,self._accessSecret,self._regionID)

    def create_database(self,dbname,character):
        request = CreateDatabaseRequest()
        request.set_accept_format('json')
        request.set_CharacterSetName(character)
        request.set_DBName(dbname)
        request.set_DBInstanceId(self._DBInstanceId)
        try:
            respone = self._client.do_action_with_exception(request)
        except:
            print('%s 数据库创建失败' % dbname)

    def check_account(self,account):
        request = DescribeAccountsRequest()
        request.set_accept_format('json')
        request.set_AccountName(account)
        request.set_DBInstanceId(self._DBInstanceId)
        try:
            respone = self._client.do_action_with_exception(request)
            account_info = json.loads(str(respone,encoding='utf-8'))
            print(account_info)
            rds_account = account_info['Accounts']['DBInstanceAccount']
            if rds_account:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def database_info(self):
        request = DescribeDatabasesRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(self._DBInstanceId)
        respone = self._client.do_action_with_exception(request)
        print(respone)

    def create_account(self,username,password,is_super=False):
        is_exsit = self.check_account(username)
        if is_exsit:
            print('%s 用户已存在。。。' % username)
        else:
            request = CreateAccountRequest()
            request.set_accept_format('json')
            request.set_AccountPassword(password)
            request.set_AccountName(username)
            request.set_DBInstanceId(self._DBInstanceId)
            if is_super:
                request.set_AccountType("super")
            try:
                response = self._client.do_action_with_exception(request)
            except:
                print('数据库用户 %s 创建失败！！！' %username)

    def grant_privilege(self,account_name,dbname,addprivelege):
        '''
        权限分为  ReadOnly:只读; ReadWrite：读写；
        DDLOnly（适用于MySQL和MariaDB）：只能执行DDL
        DMLOnly（适用于MySQL和MariaDB）：只能执行DML；
        :return:
        '''

        request = GrantAccountPrivilegeRequest()
        request.set_accept_format('json')
        request.set_AccountPrivilege(addprivelege)
        request.set_DBName(dbname)
        request.set_AccountName(account_name)
        request.set_DBInstanceId(self._DBInstanceId)

        try:
            respone = self._client.do_action_with_exception(request)
        except Exception as e:
            print(e)
            print('用户授权失败')

    def revoke_privilege(self,account, dbname):
        '''
        :return:
        '''
        request = RevokeAccountPrivilegeRequest()
        request.set_accept_format('json')
        request.set_DBName(dbname)
        request.set_AccountName(account)
        request.set_DBInstanceId(self._DBInstanceId)

        try:
            respone = self._client.do_action_with_exception(request)
            print('用户 %s 移除%s库权限成功！！！' %(account,dbname))
        except Exception as e:
            print(e)
            print('用户 %s 移除%s库权限失败！！！' %(account,dbname))


    def reset_password(self,account,password):
        request = ResetAccountPasswordRequest()
        request.set_accept_format('json')
        request.set_AccountPassword(password)
        request.set_AccountName(account)
        request.set_DBInstanceId(self._DBInstanceId)
        try:
            respone = self._client.do_action_with_exception(request)
            print('%s 密码重置成功!!!' % account)
        except Exception as e:
            print(e)
            print('%s 密码重置失败!!!' % account)


    def delete_account(self,account):
        request = DeleteAccountRequest()
        request.set_accept_format('json')
        request.set_AccountName(account)
        request.set_DBInstanceId(self._DBInstanceId)

        try:
            respone = self._client.do_action_with_exception(request)
            print('%s 删除成功!!!' % account)
        except Exception as e:
            print(e)
            print('%s 删除失败!!!' % account)


    def instance_info(self):
        request = DescribeDBInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(self._DBInstanceId)

        try:
            respone = self._client.do_action_with_exception(request)

            info = json.loads(str(respone,encoding='utf-8'))
            rds_info = {}
            rds_dict = info['Items']
            total_storage = rds_dict['DBInstanceAttribute'][0]['DBInstanceStorage']
            disk_usage = rds_dict['DBInstanceAttribute'][0]['DBInstanceDiskUsed']
            rds_memory = rds_dict['DBInstanceAttribute'][0]['DBInstanceMemory']/1024
            rds_cpu = rds_dict['DBInstanceAttribute'][0]['DBInstanceCPU']
            rds_engine = rds_dict['DBInstanceAttribute'][0]['Engine']
            expire_time_str = rds_dict['DBInstanceAttribute'][0]['ExpireTime']

            expire_time = datetime.datetime.strptime(expire_time_str,'%Y-%m-%dT%H:%M:%SZ').date()
            current_time =datetime.datetime.today().date()
            expire_day = str(expire_time - current_time).split()[0]

            rds_info['total_storage'] = total_storage
            rds_info['disk_usage'] = disk_usage/1024/1024/1024
            rds_info['rds_memory'] = rds_memory
            rds_info['rds_cpu'] = rds_cpu
            rds_info['rds_engine'] = rds_engine
            rds_info['expire_day'] = expire_day
            return rds_info
        except Exception as e:
            print('获取RDS 信息失败!!!')








if __name__ == '__main__':
    rds_obj = operatingRds('LTAIAbLLEtRMTqRj','ojif3msOAhfvclWox1vowPUjZXIYxO','rm-bp17b66dxluo22n60')
    #print(rds_obj.check_account('zdjt_super'))
    rds_obj.database_info()
    #rds_obj.create_database('python_test','utf8')
    #rds_obj.create_account('python_test','QWE123!@#')
    #rds_obj.grant_privilege('python_test','python_test','ReadOnly')
    #rds_obj.revoke_privilege('python_test','python_test')
    #rds_obj.delete_account('python_test')
    # rds_info = rds_obj.instance_info()
    # print(rds_info)
    #rds_obj.check_account('huangx_zdjt')
    rds_id = checkZoneRdsID('LTAIAbLLEtRMTqRj','ojif3msOAhfvclWox1vowPUjZXIYxO')
    rds_instance = rds_id.get_rds_id('子弹借条')
    print(rds_instance)