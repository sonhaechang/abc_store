# Generated by Django 4.1.2 on 2022-11-14 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_managers_alter_orderitem_managers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='last_name',
            new_name='buyer_name',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='detail_address',
            new_name='detail_addr',
        ),
        migrations.RemoveField(
            model_name='order',
            name='first_name',
        ),
    ]
