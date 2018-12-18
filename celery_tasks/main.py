from celery import Celery
# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiMall.settings'

# 创建Celery应用对象
app = Celery("meiduo")

# 加载celery配置   config_from_object加载配置的方法
app.config_from_object('celery_tasks.config')

# 注册异步任务到Celery
# 自动会从包中读取tasks.py模块中的任务
app.autodiscover_tasks(["celery_tasks.sms"])

# 最终在终端运行这个main文件
# celery -A 应用包名 worker  -l info

# 我们当前项目，在后端项目根目录下运行
# celery -A celery_tasks.main worker -l info