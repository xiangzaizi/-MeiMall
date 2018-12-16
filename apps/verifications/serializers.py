from django_redis import get_redis_connection
from rest_framework import serializers
from redis import RedisError
import logging


# 获取在配置文件中定义的logger, 用来记录日志
logger = logging.getLogger('meiduo')

# GET /image_code/<image_code_id>/
class ImageCodeCheckSerializer(serializers.Serializer):
    """检查图片验证码的序列化器"""

    # 1. 声明验证规则[验证图片验证码]
    # 验证码编号: serializers.UUIDField专门用于验证码UUID的格式内容
    image_code_id = serializers.UUIDField()
    image_code = serializers.CharField(max_length=4, min_length=4)

    # 2.编写验证代码 validate validate_xxx
    def validate(self, attrs):
        # 2.1 获取实际校验的数据
        image_code_id = attrs['image_code_id']  # 验证码id
        image_code = attrs['image_code']  # 页面显示的验证码

        # 获取redis操作对象
        redis_conn = get_redis_connection('verify_codes')
        # 从redis中获取真实的图片验证码,怎么获取当然是通过当初以image_code_id名字获取呢!
        real_image_code_text = redis_conn.get('img_%s' % image_code_id)

        # 如果图片验证码过期或者没有
        if not real_image_code_text:
            raise serializers.ValidationError('图片验证码无效')

        # 验证码只能使用一次, 所以每次来到这里的时候,我们需要删除
        # 直接从redis中删除对应的验证码数据就可以
        try:
            # 删除一个不存在的键, 会报错(已过期),删除为了避免爬虫暴力破解,重复使用该验证码
            redis_conn.delete('img_%s' % image_code_id)
        except RedisError as e:
            logger.error(e)

        # 对比图片验证码
        # 因为直接从redis中获取到的数据是bytes类型, 需要转码
        real_image_code_text = real_image_code_text.decode()

        if real_image_code_text.lower() != image_code.lower():
            raise serializers.ValidationError('图片验证码错误')

        # 检查是否在60s内有发送记录
        # 在redis中维护一个表示用户发送短信记录的标示 send_flag_<mobile> 60s
        # send_flag_<mobile> 1,
        # 没有send_flag_<mobile> = None, 表示60s内内没有发过
        # 默认情况下,attrs获取到的是query_params
        # 在序列化器中可以通过, self.context["view"].kwargs["变量名"] 提起视图信息
        mobile = self.context['view'].kwargs.get('mobile')
        if mobile:
            send_flag = redis_conn.get('send_flag_%s' % mobile)

            if send_flag:  #
                raise serializers.ValidationError('请求次数过于频繁')
        # 3. 返回验证数据
        return attrs






