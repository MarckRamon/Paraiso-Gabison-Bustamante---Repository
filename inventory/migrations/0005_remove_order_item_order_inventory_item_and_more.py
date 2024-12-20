# Generated by Django 5.1.2 on 2024-11-20 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_remove_inventoryitem_expiry_days_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.AddField(
            model_name='order',
            name='inventory_item',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, to='inventory.inventoryitem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Preparing', 'Preparing'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed'), ('Arrived', 'Arrived')], default='Preparing', max_length=20),
        ),
    ]
