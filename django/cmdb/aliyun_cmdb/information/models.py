from django.db import models

# Create your models here.


class ProjectInfo(models.Model):
    p_name = models.CharField(max_length=128,unique=True,verbose_name="项目名")
    p_abbr = models.CharField(max_length=16,verbose_name="项目缩写",null=True)
    ali_account = models.CharField(max_length=64,verbose_name="阿里云账号")
    ali_secrts = models.CharField(max_length=64,verbose_name="阿里云密码")
    ali_region = models.CharField(max_length=32,default='cn-hangzhou',verbose_name="阿里云区域")
    ali_keyid = models.CharField(max_length=64,verbose_name="阿里云ID")
    ali_keysecrt = models.CharField(max_length=64,verbose_name="阿里云Secrts")
    ali_contact = models.CharField(max_length=64,verbose_name="阿里云联系人")
    ali_balance = models.IntegerField(null=True,verbose_name="账户余额")
    p_status = models.CharField(max_length=32,verbose_name="项目状态")
    p_date = models.DateField(verbose_name="上线时间")

class Balance(models.Model):
    pass

class RdsInfo(models.Model):
    p_name = models.CharField(max_length=64,unique=True,verbose_name="项目名")
    r_aid = models.CharField(max_length=64,verbose_name="实例")
    r_engine = models.CharField(max_length=32,verbose_name="类型")
    r_usage = models.IntegerField(verbose_name="磁盘使用量")
    r_totalusage = models.IntegerField(verbose_name="磁盘总量")
    r_memory = models.IntegerField(verbose_name="内存")
    r_cpu = models.IntegerField(verbose_name="CPU",default=None)
    r_expire = models.IntegerField(verbose_name="过期剩余时间")



class EcsInfo(models.Model):
    p_name = models.CharField(max_length=32,null=True,verbose_name="项目名")
    instanceId = models.CharField(max_length=32,unique=True,verbose_name="ECS实例id",null=True)
    instanceName = models.CharField(max_length=32,verbose_name="ECS实例名字",null=True)
    cpu = models.IntegerField(verbose_name="cpu 个数",null=True)
    memory = models.IntegerField(verbose_name="内存",null=True)
    pivIp = models.CharField(max_length=32,verbose_name="私有IP",null=True)
    pubIp = models.CharField(max_length=32,verbose_name="公有IP",null=True)
    status = models.CharField(max_length=32,verbose_name="实例状态",null=True)
    expireTime = models.CharField(max_length=32,verbose_name="过期时间",null=True)

class SslInfo(models.Model):
    pass

class DomainInfo(models.Model):
    pass

class User(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=64,verbose_name="密码")
    email = models.EmailField()
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=True,verbose_name="修改时间")

    def __str__(self):
        self.username

