# Generated by Django 2.2.6 on 2022-01-20 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('good_purchase', '0002_groupapply_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodtype',
            name='type_name',
            field=models.CharField(max_length=20, unique=True, verbose_name='类型名称'),
        ),
        migrations.AlterField(
            model_name='groupapply',
            name='remarks',
            field=models.CharField(max_length=255, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='groupapply',
            name='status',
            field=models.IntegerField(choices=[(1, '已退回'), (2, '在使用'), (3, '退回中'), (4, '购买中')], verbose_name='物资状态'),
        ),
    ]
