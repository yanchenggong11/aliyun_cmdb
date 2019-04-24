# Generated by Django 2.0 on 2019-03-19 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rdsinfo',
            name='r_cpu',
            field=models.IntegerField(default=None, verbose_name='CPU'),
        ),
        migrations.AlterField(
            model_name='rdsinfo',
            name='r_expire',
            field=models.IntegerField(verbose_name='过期剩余时间'),
        ),
        migrations.AlterField(
            model_name='rdsinfo',
            name='r_memory',
            field=models.IntegerField(verbose_name='内存'),
        ),
        migrations.AlterField(
            model_name='rdsinfo',
            name='r_totalusage',
            field=models.IntegerField(verbose_name='磁盘总量'),
        ),
        migrations.AlterField(
            model_name='rdsinfo',
            name='r_usage',
            field=models.IntegerField(verbose_name='磁盘使用量'),
        ),
    ]
