# Generated by Django 3.0 on 2019-12-21 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_num',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='手机号'),
        ),
    ]
