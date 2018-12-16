from django.db import models

class BaseModel(models.Model):
    """基本模型补充公共字段"""
    create_time = models.DateField(auto_now_add=True,verbose_name="创建时间")
    update_time = models.DateField(auto_now=True,verbose_name="更新时间")

    class Meta:
        # 声明当前模型是一个只能被继承的抽象类，
        # 到时Django数据迁移就不会创建这个模型对应的baseModel表了
        abstract = True