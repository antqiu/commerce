# Generated by Django 4.1.3 on 2022-12-05 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_comment_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='time',
        ),
    ]
