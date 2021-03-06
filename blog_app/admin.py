from django.contrib import admin
from .models import Article,Category,Tag
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

admin.site.register(Article,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
