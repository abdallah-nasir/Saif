# Generated by Django 3.2.4 on 2021-06-20 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tech_Parts', '0003_product_const'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='const',
        ),
        migrations.AlterField(
            model_name='product',
            name='processor',
            field=models.ManyToManyField(to='Tech_Parts.Processor'),
        ),
    ]
