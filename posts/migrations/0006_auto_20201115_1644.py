# Generated by Django 2.2.6 on 2020-11-15 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_delete_newpost'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'группа', 'verbose_name_plural': 'группы'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',), 'verbose_name': 'пост', 'verbose_name_plural': 'посты'},
        ),
    ]