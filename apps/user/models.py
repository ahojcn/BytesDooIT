from django.db import models


class User(models.Model):
    """
    用户基础信息
    """
    username = models.CharField(max_length=128, unique=True, verbose_name='用户名', null=False)
    email = models.CharField(max_length=128, unique=True, verbose_name='邮箱')
    phone_num = models.CharField(max_length=20, null=True, blank=True, verbose_name='手机号')
    password = models.CharField(null=False, blank=False, max_length=128, verbose_name='密码')
    USER_GENDER_CHOICES = ((0, '保密'), (1, '男'), (2, '女'))
    gender = models.SmallIntegerField(default=0, choices=USER_GENDER_CHOICES, verbose_name='性别')
    description = models.CharField(null=True, blank=True, max_length=256, default='这个人很懒，什么都没留下。', verbose_name='简介/签名')
    reg_datetime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    avatar_path = models.CharField(default='media/img/default_avatar.png', max_length=1024, verbose_name='头像地址')
    last_login_datetime = models.DateTimeField(auto_now=True, verbose_name='上次登录时间')
    level = models.SmallIntegerField(default=1, verbose_name='等级')
    exp_val = models.IntegerField(default=1, verbose_name='经验值')
    food_num = models.IntegerField(default=10, verbose_name='辣条数量')
    live_token = models.CharField(null=True, blank=False, max_length=128, verbose_name='直播token')
    is_mute = models.BooleanField(default=False, verbose_name='是否被禁言')
    is_active = models.BooleanField(default=False, verbose_name='是否已激活')
    extra_data = models.TextField(default='', verbose_name='其他信息')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'user'
        verbose_name = '用户基础信息'
        verbose_name_plural = verbose_name


class UserAuthority(models.Model):
    """
    用户权限表
    """
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=False, blank=False, verbose_name='用户id')
    video = models.BooleanField(default=False, verbose_name='上传视频权限')
    post = models.BooleanField(default=False, verbose_name='新增文章权限')
    resume = models.BooleanField(default=False, verbose_name='新增简历权限')
    live = models.BooleanField(default=False, verbose_name='直播权限')
    recruitment = models.BooleanField(default=False, verbose_name='新增招聘信息')
    comment = models.BooleanField(default=False, verbose_name='新增评论')
    interview = models.BooleanField(default=False, verbose_name='面试权限')
    extra_data = models.TextField(default='', verbose_name='其他信息')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'user_authority'
        verbose_name = '用户权限'
        verbose_name_plural = verbose_name


class UserResume(models.Model):
    """
    用户简历表
    """
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=False, blank=False, verbose_name='用户id')
    outline = models.TextField(default='', verbose_name='简介')
    educational = models.TextField(default='', verbose_name='教育经历')
    job_exp = models.TextField(default='', verbose_name='工作经历')
    purpose = models.TextField(default='', verbose_name='求职意向')
    project = models.TextField(default='', verbose_name='项目经历')
    honor = models.TextField(default='', verbose_name='获奖情况')
    skill = models.TextField(default='', verbose_name='个人技能')
    other_info = models.TextField(default='', verbose_name='其他信息')
    extra_data = models.TextField(default='', verbose_name='其他信息')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'user_resume'
        verbose_name = '用户简历'
        verbose_name_plural = verbose_name


class UserAuthenticationInfo(models.Model):
    """
    用户认证信息表
    """
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=False, blank=False, verbose_name='用户id')
    AUTH_TO_CHOICES = ((0, '直播'), (1, '招聘'))
    auth_to = models.SmallIntegerField(choices=AUTH_TO_CHOICES, verbose_name='认证干什么')
    id_card_photo_path = models.CharField(null=False, blank=False, max_length=1024, verbose_name='身份证照片')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='认证提交时间')
    AUTH_RESULT = ((0, '未审核'), (1, '审核通过'), (2, '审核不通过'))
    result = models.SmallIntegerField(choices=AUTH_RESULT, default=0, verbose_name='审核结果')
    fail_reason = models.CharField(default='', max_length=1024, verbose_name='失败原因')
    extra_data = models.TextField(default='', verbose_name='其他信息')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'user_authentication_info'
        verbose_name = '用户认证信息'
        verbose_name_plural = verbose_name
