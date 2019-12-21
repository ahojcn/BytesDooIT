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
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='文章标题')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('like_count', models.IntegerField(default=0, verbose_name='点赞数')),
                ('is_draft', models.BooleanField(default=False, verbose_name='是否为草稿')),
                ('food_count', models.IntegerField(default=0, verbose_name='获得辣条数')),
                ('extra_data', models.TextField(default='', verbose_name='额外信息')),
                ('is_delete', models.BooleanField(default=False, verbose_name='已删除')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_post', to='user.User', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='标签名')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('extra_data', models.TextField(default='', verbose_name='额外信息')),
                ('is_delete', models.BooleanField(default=False, verbose_name='已删除')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_post_tag', to='post.Post', verbose_name='文章id')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_post_tag', to='user.User', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '文章标签',
                'verbose_name_plural': '文章标签',
                'db_table': 'post_tag',
            },
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='分类名')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('extra_data', models.TextField(default='', verbose_name='额外信息')),
                ('is_delete', models.BooleanField(default=False, verbose_name='已删除')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_post_category', to='post.Post', verbose_name='文章id')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_post_category', to='user.User', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
                'db_table': 'post_category',
            },
        ),
    ]
