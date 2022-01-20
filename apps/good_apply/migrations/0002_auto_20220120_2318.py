# Generated by Django 2.2.6 on 2022-01-20 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('good_apply', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='result',
            field=models.IntegerField(choices=[(1, '通过'), (2, '未通过')], verbose_name='审核结果'),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewer_identity',
            field=models.IntegerField(choices=[(1, '组长'), (2, '秘书')], verbose_name='审核人身份'),
        ),
    ]
