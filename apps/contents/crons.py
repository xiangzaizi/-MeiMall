# 查询当前页面需要的数据
from collections import OrderedDict
from django.conf import settings
from django.template import loader
import os
import time


from apps.contents.models import ContentCategory
from apps.goods.utils import get_categories

def generate_static_index_html():
    """
    生成静态的主页html文件
    """
    print('%s: generate_static_index_html' % time.ctime())

    # 商品频道及分类菜单
    categories = get_categories()

    # 广告内容
    contents = {}
    # 获取所有的广告分类
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True)

    # 渲染模板
    context = {
        'categories': categories,
        'contents': contents
    }

    # django 提供的视图加载器loader获取模板内容
    template = loader.get_template('index.html')
    html_text = template.render(context)
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')
    with open(file_path, 'w') as f:
        f.write(html_text)