from django.db.models import Count

from ..models import Article,Category,Tag
from django import template
# 这一页是自定义模板标签，其实就是页面上可直接调用的函数
# 为了能够通过 {% get_recent_posts %} 的语法在模板中调用这个函数
# 必须按照 Django 的规定注册这个函数为模板标签
# 然后在模板中导入这个文件{% load blog_app_tags %}
register = template.Library()

#得到五个最近的文章标签
@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-created_time')[:num]

#按照日期归档标签
@register.simple_tag
def archives():
    return Article.objects.dates('created_time', 'month', order='DESC')


#分类标签
# @register.simple_tag
# def get_categories():
#     return Category.objects.all()

@register.simple_tag
def get_categories():
# annotate用于对两个相关的model进行连接
    return Category.objects.annotate(num_article = Count('article')).filter(num_article__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_intag = Count('article')).filter(num_intag__gt = 0)