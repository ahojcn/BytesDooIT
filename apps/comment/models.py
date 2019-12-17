from django.db import models

from apps.user.models import User
from apps.post.models import Post
from apps.video.models import Video


class Comment(models.Model):
    """
    评论表
    """
    COMMENT_TO_CHOICES = ((0, '视频'), (1, '文章'))
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_comment', null=False, blank=False,
                                verbose_name='用户id')
    to = models.IntegerField(choices=COMMENT_TO_CHOICES, null=False, blank=False, verbose_name='视频还是文章评论')
    post_id = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='post_comment', null=True, blank=True,
                                verbose_name='文章id')
    video_id = models.ForeignKey(to=Video, on_delete=models.CASCADE, related_name='video_comment', null=True,
                                 blank=True)
    content = models.CharField(default='', max_length=1024, null=False, blank=True, verbose_name='评论内容')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    extra_data = models.TextField(default='', verbose_name='额外信息')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class CommentReply(models.Model):
    """
    评论回复表
    """
    comment_id = models.ForeignKey(to=Comment, on_delete=models.DO_NOTHING, null=False, blank=False,
                                   verbose_name='评论id')
    user_id = models.ForeignKey(to=User, related_name='comment_user', on_delete=models.DO_NOTHING, null=False,
                                blank=False, verbose_name='用户id')
    replay_to = models.ForeignKey(to=User, related_name='replay_to_user', on_delete=models.DO_NOTHING, null=False,
                                  blank=False, verbose_name='被回复人id')
    content = models.TextField(default='', verbose_name='回复内容')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')
    extra_data = models.TextField(default='', verbose_name='额外信息')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'comment_reply'
        verbose_name = '评论回复'
        verbose_name_plural = verbose_name
