from django.db import models

# 时间抽象表


class TimeBasic(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    create_user = models.CharField(max_length=120, verbose_name='创建用户', null=True, blank=True)
    update_user = models.CharField(max_length=120, verbose_name='更新用户', null=True, blank=True)

    class Meta:
        abstract = True
