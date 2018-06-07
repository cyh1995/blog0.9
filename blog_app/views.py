#视图函数需要从模板中获得参数
from msilib.schema import ListView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from .models import Article,Category,Tag
from django.shortcuts import render,get_object_or_404
import markdown
from comments_app.forms import CommentForm
from django.views.generic import ListView,DetailView
# Create your views here.


# def index(request):
#     article_list=Article.objects.all().order_by('-created_time')
#     #分页方法
#     paginator = Paginator(article_list,2)
#     page = request.GET.get('page')
#     try:
#         contacts = paginator.page(page)
#     except PageNotAnInteger:
#         # 如果用户请求的页码号不是整数，显示第一页
#         contacts = paginator.page(1)
#     except EmptyPage:
#         # 如果用户请求的页码号超过了最大页码号，显示最后一页
#         contacts = paginator.page(paginator.num_pages)
#     #可以通过HttpPesponse来返回字符串，但一般要调用render函数
#     #参数是request,'模板地址',传值(dict形式)
#     return render(request, 'blog/index.html', context={'article_list':article_list,'contacts':contacts})

class IndexView(ListView):
    model = Article
    template_name = "blog/index.html"
    context_object_name = "article_list"
    paginate_by = 2









# def detail(request,pk):
#     article = get_object_or_404(Article, pk=pk)
#     #文字格式编辑引入了markdown包
#     article.views_add()
#     article.save()
#     article.body = markdown.markdown(article.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#
#
#     form = CommentForm()
#     comment_list = article.comment_set.all()
#     context = {'article': article,
#                        'form':form,
#                        'comment_list': comment_list
#               }
#     return render(request, 'blog/detail.html', context=context)
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
    # get 方法返回的是一个 HttpResponse 实例
    # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
    # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
    def get(self , request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
            response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
            self.object.views_add()
        # 视图必须返回一个 HttpResponse 对象
            return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(ArticleDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post
    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context




# 时间归档分类，引入filter可以按条件筛选
# 其中create_time是python objects里自生成的date对象
# def archives(request,year,month):
#     article_list = Article.objects.filter(created_time__year=year,
#                                      created_time__month=month).order_by('-created_time')
#     return render(request,'blog/index.html',context={'article_list':article_list})

class ArchivesView(ListView):
    model = Article
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        return super(ArchivesView,self).get_queryset().filter(created_time__year=year,
                                     created_time__month=month).order_by('-created_time')

# def category(request,pk):
#     cate=get_object_or_404(Category,pk=pk)
#     article_list = Article.objects.filter(category=cate).order_by('-created_time')
#     return render(request,'blog/index.html',context={'article_list':article_list})

class CategoryView(ListView):
    model = Article
    template_name = "blog/index.html"
    context_object_name = "article_list"
    #复写,该方法默认获取全部列表数据。
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate).order_by('-created_time')

class TagView(ListView):
    model = Article
    template_name = 'blog/index.html'
    #可以用这两个不同的命名在同一页面渲染不同的东西
    #如Tag_list然后在index模板里写Tag_list,这样不会影响之前article_list的显示，当不调用时什么也不会显示。
    context_object_name = "article_list"
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tag=tag).order_by('-created_time')




# def listing(request):
#     article_list = Article.objects.all().order_by('-created_time')
#     paginator = Paginator(article_list,2)
#     page = request.GET.get('page')
#     try:
#         contacts = paginator.page(page)
#     except PageNotAnInteger:
#         # 如果用户请求的页码号不是整数，显示第一页
#         contacts = paginator.page(1)
#     except EmptyPage:
#         # 如果用户请求的页码号超过了最大页码号，显示最后一页
#         contacts = paginator.page(paginator.num_pages)
#
#     return render(request, 'list.html', {'contacts': contacts})
