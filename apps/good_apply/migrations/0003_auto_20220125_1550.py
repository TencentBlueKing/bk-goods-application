# Generated by Django 2.2.6 on 2022-01-25 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('good_apply', '0002_auto_20220120_2318'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apply',
            options={'verbose_name': '申请表', 'verbose_name_plural': '申请表'},
        ),
        migrations.AlterModelOptions(
            name='position',
            options={'verbose_name': '地区表', 'verbose_name_plural': '地区表'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': '申请审核表', 'verbose_name_plural': '申请审核表'},
        ),
        migrations.AlterModelOptions(
            name='secretary',
            options={'verbose_name': '秘书表', 'verbose_name_plural': '秘书表'},
        ),
    ]
