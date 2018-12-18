from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User


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