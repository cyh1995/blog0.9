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
from django.urls import path,include


#在总urls文件中使用命名空间。namespace可以更好的对各app的url进行区分
#之后只需要在各app的url中对应相应的namespace即可。


urlpatterns = [
    path('admin/', admin.site.urls),
    #path中第一个空缺可以填入总的url，对应app的url字符串拼在这后面。
    path('',include('blog_app.urls',namespace='blog_app')),
    path('',include('comments_app.urls',namespace='comments_app')),
]
