# Generated by Django 3.2.23 on 2024-04-11 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_bank_details_crypto_discount_table_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='confirmation_no',
        ),
    ]
