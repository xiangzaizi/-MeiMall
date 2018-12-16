from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework import status

from apps.verifications.serializers import ImageCodeCheckSerializer
from libs.captcha.captcha import captcha
from . import constants

# /image_code/uuid
class ImageCodeView(APIView):
    """图片验证码"""
    def get(self, request, image_code_id):
        # 1. 调用第三方库生成图片验证码
        text, image = captcha.generate_captcha()

        # 2.保存图片验证码文本信息到redis里面
        # 通过python与redis的交互连接将数据存入redis中
        # 2.1 获取redis连接对象, 参数就是配置文件中的redis参数
        redis_conn = get_redis_connection('verify_codes')
        # 2.2 保存图片验证码到redis中
        # redis_conn.setex('变量名', '有效期', '值')
        # image_code_id 用户的uuid
        redis_conn.setex('img_%s' % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 3. 响应返回图片
        return HttpResponse(image, content_type="images/jpg")


class SMSCodeView(GenericAPIView):
    # GenericAPIView 可以声明当前类的序列化器
    """短信验证码"""
    # 声明当前视图类的序列化器,直接拿序列化器中的序列化器
    # GET /sms_code/(?P<mobile>.+)/?image_code
    serializer_class = ImageCodeCheckSerializer
    def get(self, request, mobile):
        # 1. 在序列化器中 检查图片验证码
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 2. 生成短信验证码

        # 3. 保存短信验证码与发送记录

        # 4. 发送短信

        # 5. 返回响应
        return Response({"message": "OK"}, status.HTTP_200_OK)




