# Generated by Django 5.1.1 on 2024-11-20 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_admin_firstname_admin_lastname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='firstname',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='admin',
            name='lastname',
            field=models.CharField(max_length=150),
        ),
    ]
