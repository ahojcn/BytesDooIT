# Generated by Django 3.0 on 2020-01-06 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='video_id',
            new_name='video',
        ),
        migrations.DeleteModel(
            name='CommentReply',
        ),
    ]
