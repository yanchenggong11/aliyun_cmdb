# Generated by Django 2.0 on 2019-03-26 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0003_auto_20190326_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecsinfo',
            name='p_name',
            field=models.CharField(max_length=32, null=True, verbose_name='项目名'),
        ),
    ]
