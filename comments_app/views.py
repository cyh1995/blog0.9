from django.shortcuts import render,get_object_or_404,redirect
from blog_app.models import Article

from .models import Comment
from .forms import CommentForm
# Create your views here.
def article_comment(request, article_pk):
    #得到pk=article_pk的Article或404
    article = get_object_or_404(Article,pk=article_pk)
    # 只有当用户的请求为 post 时才需要处理表单数据
    if request.method=='POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的form就生成了。
        form = CommentForm(request.POST)
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            Comment.like_add()
            # redirect 既可以接收一个 URL 作为参数，
            # 也可以接收一个模型的实例作为参数（例如这里的 article）。
            # 这个实例必须实现了 get_absolute_url 方法，这样会根据 get_absolute_url 方法返回的 URL 值进行重定向。
            return redirect(article)

        else:
         # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Article），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 article.comment_set.all() 方法，
            # 这个用法有点类似于 Article.objects.all()
            # 其作用是获取这篇 article 下的的全部评论，
            # 因为 Article 和 Comment 是 ForeignKey 关联的，因此使用 comment_set.all() 反向查询全部评论。
            comment_list = article.comment_set.all()
            context = {'article': article,
                       'form':form,
                       'comment_list': comment_list
                      }
            return render(request,'blog/detail.html', context=context)
    return redirect(article)

