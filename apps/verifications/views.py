from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework import status
import random

from apps.verifications.serializers import ImageCodeCheckSerializer
from libs.captcha.captcha import captcha
from libs.yuntongxun.sms import CCP
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
        sms_code = "%06d" % random.randint(0, 999999)

        # 3. 保存短信验证码与发送记录
        redis_conn = get_redis_connection('verify_codes')
        # 当项目中连续出现多条操作redis的语句时，可以使用pipeline管道命令，把多条操作
        # 组合到一次发送给redis，可以有效提高执行效率
        # 通过pipeline方法，获取管道对象，管道对象继承于redis连接对象
        # 所以redis中本身支持方法属性，pipeline对象也可以操作
        pl = redis_conn.pipeline()
        pl.multi()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 发送短信的标志，维护60秒
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()  # 把上面组装的操作一并执行

        # 4. 发送短信
        # ccp = CCP()
        # time = str(constants.SMS_CODE_REDIS_EXPIRES/60)
        # ccp.send_template_sms(mobile, [sms_code, time], constants.SMS_TEMP_ID)

        # 5. 返回响应
        return Response({"message": "OK"}, status.HTTP_200_OK)




