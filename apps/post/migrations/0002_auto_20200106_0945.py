# Generated by Django 3.0 on 2020-01-06 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcategory',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='postcategory',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='posttag',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='posttag',
            old_name='user_id',
            new_name='user',
        ),
    ]
