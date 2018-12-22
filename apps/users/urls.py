from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token  # 导入jwt实现的登录视图功能
from .views import UserNameCountView, MobileCountView, UserView
urlpatterns = [
    # 用户名和手机号码的唯一性校验
    url(r'^usernames/(?P<username>\w{5,20})/count/$', UserNameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3456789]\d{9})/count/$', MobileCountView.as_view()),

    # 用户注册
    url(r'^user/$', UserView.as_view()),
    # 用户登录功能obtain_jwt_token的实现
    url(r'^authorizations/$', obtain_jwt_token, name='authorizations')

]
