# Generated by Django 3.0 on 2019-12-21 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterviewRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_note', models.TextField(default='', verbose_name='面试者笔记')),
                ('interviewer_note', models.TextField(default='', verbose_name='面试官笔记')),
                ('share_note', models.TextField(default='', verbose_name='共享笔记')),
                ('interviewer_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='interviewer', to='user.User', verbose_name='面试官id')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='interview_user', to='user.User', verbose_name='面试者id')),
            ],
            options={
                'verbose_name': '面试房间',
                'verbose_name_plural': '面试房间',
                'db_table': 'interview_room',
            },
        ),
    ]
