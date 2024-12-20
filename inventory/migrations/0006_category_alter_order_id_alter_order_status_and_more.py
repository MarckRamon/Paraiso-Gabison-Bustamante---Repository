# Generated by Django 5.1.2 on 2024-11-21 02:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_remove_order_item_order_inventory_item_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Electronics', 'Electronics'), ('Clothing', 'Clothing'), ('Food', 'Food'), ('Furniture', 'Furniture'), ('Toys', 'Toys')], max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Preparing', 'Preparing'), ('Cancelled', 'Cancelled'), ('Arrived', 'Arrived')], default='Preparing', max_length=20),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.category'),
        ),
    ]
