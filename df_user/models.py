#coding=utf-8
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    ushou = models.CharField(max_length=20,default='')#定义一个默认值 不需重新迁移，这属于python层面的操作，无关数据库
    uaddress = models.CharField(max_length=100,default='')#只有更改到数据库的东西才需迁移
    uyoubian = models.CharField(max_length=6,default='')
    uphone = models.CharField(max_length=11,default='')
    #default,blank 是pthon层面的约束，不影响数据库标结构


