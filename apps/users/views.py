from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from apps.verifications.serializers import ImageCodeCheckSerializer
from . import serializers
from .utils import get_user_by_account
import re

class UserNameCountView(APIView):
    """
    用户名数量
    """
    # usernames/(?P<username>\w{5,20})/count/
    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()
        data = {
            'username': username,
            'count': count
        }
        return Response(data)


class MobileCountView(APIView):
    """
    手机号数量
    """
    # mobiles/(?P<mobile>1[345789]\d{9})/count
    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile': mobile,
            'count': count
        }
        return Response(data)


class UserView(CreateAPIView):
    """用户注册"""
    serializer_class = serializers.CreateUserSerializer


class SMSCodeTokenView(GenericAPIView):
    """通过账号获取临时访问票据"""
    serializer_class = ImageCodeCheckSerializer
    def get(self, request, account):
        """
        :account:手机号码或者账号名
        :return: access_token 或者None
        """
        # 1. 校验图形验证码是否正确
        # query_params, 地址栏中后面的查询字符串
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 2. 根据提交过来的account获取用户信息
        user = get_user_by_account(account)
        if user is None:
            return Response({"message": "用户不存在!"}, status=status.HTTP_404_NOT_FOUND)

        # 3. 生成access_token, 从模型中创建此方法,用户可以直接调用
        access_token = user.generate_password_token()

        # 手机号是用户的敏感信息,所以需要处理一下
        # \1表示第一个括号内容,****隐藏用户信息,\2最后一个括号的信息.
        mobile = re.sub(r'(\d{3})\d{4}(\d{4})', r'\1****\2', user.mobile)

        # 4. 返回响应数据
        return Response({
            'mobile': mobile,
            'access_token': access_token
        })
