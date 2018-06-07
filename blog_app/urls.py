"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from  blog_app import views

#视图函数命名空间。对应总urls中的视图空间。
#如有参数则需要在对应的视图函数中做处理，如下<int:pk>的pk会在views的detail中处理
#name作用类似于ID
app_name='blog_app'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('detail/<int:pk>/',views.ArticleDetailView.as_view(),name='detail'),
    path('index/',views.IndexView.as_view(),name='index'),
    path('archives/<int:year>/<int:month>/',views.ArchivesView.as_view(),name='archives'),
    path('category/<int:pk>/',views.CategoryView.as_view(),name='Category'),
    path('tag/<int:pk>/',views.TagView.as_view(),name = 'Tag'),
]
