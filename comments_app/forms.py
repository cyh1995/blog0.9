# 通过调用这个继承与form对象的类的一些方法和属性，来代替原有的前端表单
from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','url','text']
