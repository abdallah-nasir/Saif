# Generated by Django 3.2.4 on 2021-06-20 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tech_Parts', '0011_auto_20210620_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='fps_numbers',
            name='details',
            field=models.CharField(default='sad', max_length=50),
            preserve_default=False,
        ),
    ]