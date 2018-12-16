from django.conf.urls import url
from apps.verifications.views import ImageCodeView, SMSCodeView

urlpatterns = [
    url(r'^image_code/(?P<image_code_id>.+)/$', ImageCodeView.as_view()),
    url(r'^sms_code/(?P<mobile>1[3-9]\d{9})/$', SMSCodeView.as_view()),

]
