from django.db import models

from user.models import User


class InterviewRoom(models.Model):
    """
    面试房间表
    """
    interviewer_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='interviewer', null=False,
                                       blank=False,
                                       verbose_name='面试官id')
    user_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='interview_user', null=False, blank=False,
                                verbose_name='面试者id')
    user_note = models.TextField(default='', verbose_name='面试者笔记')
    interviewer_note = models.TextField(default='', verbose_name='面试官笔记')
    share_note = models.TextField(default='', verbose_name='共享笔记')

    class Meta:
        db_table = 'interview_room'
        verbose_name = '面试房间'
        verbose_name_plural = verbose_name
