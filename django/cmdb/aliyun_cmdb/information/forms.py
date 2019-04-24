#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 16:37
# @Author  : yanfei

from django import forms
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.validators import ValidationError,RegexValidator
from django.core.exceptions import ValidationError


class ProjectEditForm(forms.Form):
    p_name = forms.CharField(label='项目名')
    ali_account = forms.CharField(label='阿里云账号')
    ali_secrts = forms.CharField(label='阿里云密码')
    ali_region = forms.CharField(label='阿里云区域')
    ali_keyid = forms.CharField(label='AccessKeyID')
    ali_keysecrt = forms.CharField(label='AccessKeySecrt')
    ali_contact = forms.CharField(label='账号联系人')
    p_status = forms.CharField(label='项目状态')
    p_date = forms.DateField(label='上线时间')



class MyForm(forms.Form):
    user = forms.CharField(
        widget = widgets.TextInput(attrs={'id':'i1','class':'c1'})
    )

    gender = forms.ChoiceField(
        choices=((1,'男'),(2,'女'),),
        initial = 2,
        widget=widgets.RadioSelect
    )
    city = forms.CharField(
        initial=2,
        widget=widgets.Select(choices=((1,'上海'),(2,'北京'),))
    )
    pwd = forms.CharField(
        widget=widgets.PasswordInput(attrs={'class':'c1'},render_value=True)
    )

    phone = forms.CharField(
        validators=[RegexValidator(r'^[0-9]+$','请输入数字'),RegexValidator(r'159[0-9]+$','数字必须159开头')]
    )
