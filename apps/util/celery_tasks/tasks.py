import os

import django
from django.core import mail
from django.conf import settings
from django.template import loader
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BytesDooIT.settings')
django.setup()

app = Celery('utils.celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')


@app.task
def send_email(subject, message, to, template=None, *args):
    """
    celery task 异步发送邮件
    :param subject: 邮件标题
    :param message: 邮件正文
    :param to: 收件人列表
    :param template: html 模板
    :param args: 传给 template 的参数
    :return:
    """

    if template is not None:
        template = loader.get_template(template)
        html = template.render(*args)
        mail.send_mail(subject=subject,
                       message=message,
                       from_email=settings.EMAIL_FROM,
                       recipient_list=to,
                       html_message=html)
    else:
        mail.send_mail(subject=subject,
                       message=message,
                       from_email=settings.EMAIL_FROM,
                       recipient_list=to)
