from django.db import models

from user.models import User


class Post(models.Model):
    """
    文章表
    """
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='user_post', null=False, blank=False,
                             verbose_name='用户id')
    title = models.CharField(null=False, blank=False, max_length=1024, verbose_name='文章标题')
    content = models.TextField(null=False, blank=False, verbose_name='文章内容')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    is_draft = models.BooleanField(default=False, verbose_name='是否为草稿')
    food_count = models.IntegerField(default=0, verbose_name='获得辣条数')
    extra_data = models.TextField(default='', verbose_name='额外信息')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'post'
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class PostCategory(models.Model):
    """
    文章分类
    """
    user_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='user_post_category', null=False,
                                blank=False, verbose_name='用户id')
    post_id = models.ForeignKey(to=Post, on_delete=models.DO_NOTHING, related_name='post_post_category', null=False,
                                blank=False,
                                verbose_name='文章id')
    name = models.CharField(null=False, blank=False, max_length=32, verbose_name='分类名')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    extra_data = models.TextField(default='', verbose_name='额外信息')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'post_category'
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name


class PostTag(models.Model):
    """
    文章标签表
    """
    user_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='user_post_tag', null=False,
                                blank=False, verbose_name='用户id')
    post_id = models.ForeignKey(to=Post, on_delete=models.DO_NOTHING, related_name='post_post_tag', null=False,
                                blank=False, verbose_name='文章id')
    name = models.CharField(null=False, blank=False, max_length=32, verbose_name='标签名')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    extra_data = models.TextField(default='', verbose_name='额外信息')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'post_tag'
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name
