from django.db import models

from user.models import User


class VideoTag(models.Model):
    """
    视频标签表
    """
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='创建用户id')
    name = models.CharField(max_length=1024, verbose_name='标签名')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='标签创建时间')
    use_count = models.IntegerField(default=0, verbose_name='使用次数')
    extra_data = models.TextField(default='', verbose_name='额外信息')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'video_tag'
        verbose_name = '视频标签'
        verbose_name_plural = verbose_name


class Video(models.Model):
    """
    视频表
    """
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='用户id')
    path = models.TextField(verbose_name='视频路径')
    overview_path = models.TextField(verbose_name='封面路径')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    description = models.TextField(default='', verbose_name='视频描述/简介')
    tag = models.TextField(default='', verbose_name='标签')
    play_count = models.IntegerField(default=0, verbose_name='播放数')
    VIDEO_READY_CHOICES = ((0, '未审核'), (1, '审核通过'), (2, '审核不通过'),)
    is_ready = models.IntegerField(default=0, choices=VIDEO_READY_CHOICES, verbose_name='审核结果')
    not_ready_reason = models.CharField(max_length=1024, default='', verbose_name='审核不通过原因')
    VIDEO_STATUS = ((0, '未转码'), (1, '转码成功'), (2, '转码失败'),)
    status = models.IntegerField(default=0, choices=VIDEO_STATUS, verbose_name='视频状态')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    food_count = models.IntegerField(default=0, verbose_name='辣条数')
    extra_data = models.TextField(default='', verbose_name='额外信息')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'video'
        verbose_name = '视频'
        verbose_name_plural = verbose_name
