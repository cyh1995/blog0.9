# Generated by Django 2.0.4 on 2018-06-06 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.PositiveIntegerField(verbose_name='评论数'),
        ),
    ]
