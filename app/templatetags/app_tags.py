from django import template
from app.utils.fileUtils import *
register = template.Library()


# 在模板中通过下表访问list的元素
@register.filter(name='index')
def item_of_list(value, index):
    return value[index]


# 在模板中通过key访问dict的value
@register.filter(name='key')
def value_of_key_from_dict(value, key):
    return value.get(key)


@register.filter(name='is_office')
def if_office(value):
    if isOfficeFile(value):
        return True
    return False


@register.filter(name='base_name')
def file_base_name(value):
    return os.path.basename(value)

