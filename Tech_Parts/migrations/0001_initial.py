# Generated by Django 3.0.7 on 2021-06-05 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=11)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tech_Parts.Category')),
                ('name', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=100)),
                ('address', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
                ('price', models.PositiveIntegerField(default=0)),
                ('details', models.TextField()),
                ('code', models.CharField(blank=True, max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tech_Parts.Category')),
                ('processor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tech_Parts.Processor')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tech_Parts.Type')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('ordered', models.BooleanField(default=False)),
                ('device', models.CharField(blank=True, max_length=120, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tech_Parts.Customer')),
                ('products', models.ManyToManyField(blank=True, to='Tech_Parts.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Filters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(blank=True, max_length=120, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tech_Parts.Category')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tech_Parts.Customer')),
                ('processor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tech_Parts.Processor')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tech_Parts.Type')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.PositiveIntegerField(blank=True, null=True)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tech_Parts.Order')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tech_Parts.Supplier')),
            ],
        ),
    ]
