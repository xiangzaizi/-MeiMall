
from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^index', views.index),  # 项目初始化测试

]
