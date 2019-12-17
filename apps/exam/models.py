from django.db import models

from apps.user.models import User


class Exam(models.Model):
    """
    招聘用的笔试题表
    """
    create_user_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=False, blank=False,
                                       related_name='user_exam', verbose_name='创建者id')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='题目创建时间')
    start_datetime = models.DateTimeField(auto_now=True, verbose_name='笔试开始时间')
    end_datetime = models.DateTimeField(auto_now=True, verbose_name='笔试结束时间')
    questions = models.TextField(default='', verbose_name='题目')
    extra_data = models.TextField(default='', verbose_name='预留')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'exam'
        verbose_name = '招聘用的笔试题'
        verbose_name_plural = verbose_name


class ExamAnswer(models.Model):
    """
    笔试题答案表
    """
    exam_id = models.ForeignKey(to=Exam, on_delete=models.DO_NOTHING, null=False, blank=False,
                                related_name='exam_exam_answer', verbose_name='笔试题id')
    user_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='user_exam_answer', null=False,
                                blank=False,
                                verbose_name='答题用户id')
    answer = models.TextField(default='', verbose_name='答卷')
    start_datetime = models.DateTimeField(auto_now=True, verbose_name='答题开始时间')
    end_datetime = models.DateTimeField(auto_now=True, verbose_name='答题结束时间')
    jump_out_count = models.IntegerField(default=0, verbose_name='用户跳出页面次数')
    grade = models.IntegerField(default=-1, verbose_name='成绩')
    extra_data = models.TextField(default='', verbose_name='预留')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'exam_answer'
        verbose_name = '笔试题答案表'
        verbose_name_plural = verbose_name
