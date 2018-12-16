from collections import OrderedDict

from .models import GoodsChannel

def get_categories():
    """获取商品所有分类"""
    # 商品频道及分类菜单
    # 使用有序字典保存类别的顺序
    # categories = {
    #     1: { # 组1
    #         'channels': [{'id':, 'name':, 'url':},{}, {}...],
    #         'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
    #     },
    #     2: { # 组2
    #
    #     }
    # }
    # OrderedDict 有序字典，默认情况，在python中字典是无序的，
    # 所以如果希望在某些场合下希望我们使用的字典能有序排列，可以使用python原生提供的 OrderedDIct()
    # 声明有序字典
    categories = OrderedDict()
    # 获取保存等级分类的GoodsChannel表中所有顶级
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')

    for channel in channels:
        group_id = channel.group_id  # 当前组

        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        cat1 = channel.category  # 当前频道的类别

        # 追加当前频道
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })

        # 构建当前类别的子类别
        for cat2 in cat1.goodscategory_set.all():
            cat2.sub_cats = []
            for cat3 in cat2.goodscategory_set.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)

    return categories