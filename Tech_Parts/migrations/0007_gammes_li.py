# Generated by Django 3.0.7 on 2021-06-09 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tech_Parts', '0006_auto_20210609_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='gammes',
            name='li',
            field=models.CharField(default='a', max_length=10),
            preserve_default=False,
        ),
    ]