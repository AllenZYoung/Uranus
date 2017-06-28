from django import template
register = template.Library()

# 在模板中通过下表访问list的元素
@register.filter(name='index')
def item_of_list(value, index):
    return value[index]

# 在模板中通过key访问dict的value
@register.filter(name='key')
def value_of_key_from_dict(value, key):
    return value.get(key)
