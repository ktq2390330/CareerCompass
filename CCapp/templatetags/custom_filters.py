from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """辞書からキーに対応する値を取得するカスタムフィルター"""
    return dictionary.get(key)
