# Generated by Django 3.2.23 on 2024-04-06 05:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('title', models.CharField(max_length=1000000000, null=True)),
                ('content', models.CharField(max_length=1000000000, null=True)),
                ('image_file', models.ImageField(default='None', null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000000000, null=True)),
                ('image_file', models.ImageField(default='None', null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='contact_us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('first_name', models.CharField(max_length=1000000000, null=True)),
                ('last_name', models.CharField(max_length=1000000000, null=True)),
                ('email', models.CharField(max_length=1000000000, null=True)),
                ('subject', models.CharField(max_length=1000000000, null=True)),
                ('message', models.CharField(max_length=1000000000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ndate', models.DateField(auto_now_add=True)),
                ('email', models.CharField(max_length=1000000000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000000000, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('name', models.CharField(max_length=1000000000, null=True)),
                ('desc', models.CharField(max_length=1000000000, null=True)),
                ('image_file', models.ImageField(default='None', null=True, upload_to='media')),
                ('price', models.CharField(max_length=1000000000, null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.subcategory')),
            ],
        ),
    ]
