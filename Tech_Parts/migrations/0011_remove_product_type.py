# Generated by Django 3.0.7 on 2021-06-10 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tech_Parts', '0010_auto_20210610_0054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
    ]