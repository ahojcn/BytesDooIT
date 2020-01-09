from django.db import models

from user.models import User
from post.models import Post
from video.models import Video


class Comment(models.Model):
    """
    评论表
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_comment', null=False, blank=False,
                             verbose_name='用户')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='post_comment', null=True,
                             verbose_name='文章')
    video = models.ForeignKey(to=Video, on_delete=models.CASCADE, related_name='video_comment', null=True,
                              verbose_name='视频')
    ref = models.ForeignKey("self", null=True, blank=True, related_name='ref_comment', on_delete=models.CASCADE,
                            verbose_name='引用评论')
    content = models.CharField(default='', max_length=1024, null=False, blank=True, verbose_name='评论内容')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    unlike_count = models.IntegerField(default=0, verbose_name='反对数')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    extra_data = models.TextField(default='', verbose_name='额外信息')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
