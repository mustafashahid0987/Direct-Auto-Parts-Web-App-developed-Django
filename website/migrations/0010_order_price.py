# Generated by Django 3.2.23 on 2024-04-12 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_remove_order_confirmation_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.FloatField(max_length=1000000000, null=True),
        ),
    ]
