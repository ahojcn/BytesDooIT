from django.db import models

from apps.user.models import User, UserResume
from apps.exam.models import Exam


class RecruitmentCategory(models.Model):
    """
    招聘信息分类
    """
    name = models.CharField(null=False, blank=False, max_length=32, verbose_name='分类名')

    class Meta:
        db_table = 'recruitment_category'
        verbose_name = '招聘信息分类'
        verbose_name_plural = verbose_name


class Recruitment(models.Model):
    """
    招聘信息
    """
    user_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='user_recruitment', null=False,
                                blank=False, verbose_name='用户id')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='信息发布时间')
    company_name = models.CharField(null=False, blank=False, max_length=128, verbose_name='公司名')
    location = models.CharField(null=False, blank=False, max_length=128, verbose_name='工作地点')
    salary = models.CharField(null=False, blank=False, max_length=128, verbose_name='工资范围')
    require = models.CharField(null=False, blank=False, max_length=1024, verbose_name='工作职责')
    category_id = models.ForeignKey(to=RecruitmentCategory, on_delete=models.DO_NOTHING,
                                    related_name='recruitment_category', null=False, blank=False, verbose_name='招聘分类id')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    need_exam = models.BooleanField(default=False, verbose_name='需要笔试')
    exam_id = models.ForeignKey(to=Exam, on_delete=models.DO_NOTHING, related_name='recruitment_exam', null=True,
                                blank=False, verbose_name='笔试题id')
    extra_data = models.TextField(default='', verbose_name='额外信息')
    is_end = models.BooleanField(default=False, verbose_name='已结束')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'recruitment'
        verbose_name = '招聘信息'
        verbose_name_plural = verbose_name


class RecruitmentResume(models.Model):
    """
    招聘收到的简历
    """
    rec_id = models.ForeignKey(to=Recruitment, on_delete=models.DO_NOTHING, related_name='recruitment',
                               null=False, blank=False, verbose_name='招聘信息id')
    resume_id = models.ForeignKey(to=UserResume, on_delete=models.DO_NOTHING, related_name='resume_recruitment',
                                  null=False, blank=False, verbose_name='收到的简历id')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='投递时间')
    resume_tag = models.TextField(default='', verbose_name='此简历的标签')
    RESUME_STATUS_CHOICES = ((0, '待处理'), (1, '已查看'), (2, '不合适'), (3, '待安排面试'), (4, '已安排面试'), (5, '已面试'),)
    resume_status = models.IntegerField(default=0, choices=RESUME_STATUS_CHOICES, verbose_name='此简历的状态')
    interview_room_id = models.CharField(default='', max_length=1024, verbose_name='面试房间id')
    interview_note = models.TextField(default='', verbose_name='面试记录')
    extra_data = models.TextField(default='', verbose_name='额外信息')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'recruitment_resume'
        verbose_name = '招聘收到的简历'
        verbose_name_plural = verbose_name
