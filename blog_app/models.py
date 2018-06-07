from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

class Category(models.Model):
    #继承 models.Model 类
    name = models.CharField(max_length=100)
    #用方法生成num_article

class Tag(models.Model):
    name = models.CharField(max_length=100)

class Article(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)
    # 文章正文
    # 使用 TextField 来存储大段文本。
    body = models.TextField()
    # 文章的创建时间和最后一次修改时间
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    likes = models.PositiveIntegerField('评论数')
    views = models.PositiveIntegerField('浏览数')
    is_topped = models.BooleanField()
    # 文章摘要
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 一篇文章只能对应一个分类所以使用 ForeignKey，即一对多的关联。
    # 一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以使用 ManyToManyField多对多的关联。
    # 外键后必须添加 on_delete=models.CASCADE
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    # 得到Url的方法，第一个参数的值是 'blog_app:detail'，意思是 blog_app 应用下的 name=detail 的函数
    # 传回ID

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog_app:detail',kwargs={'pk':self.pk})
    def test(self):
        return self.tags
    def views_add(self):
        self.views += 1
        self.save(update_fields=['views'])
    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # 调用父类的 save 方法将数据保存到数据库中
        super(Article, self).save(*args, **kwargs)

