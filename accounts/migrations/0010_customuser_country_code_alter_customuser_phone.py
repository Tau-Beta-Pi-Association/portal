# Generated by Django 5.0.6 on 2024-07-15 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_customuser_country_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='country_code',
            field=models.CharField(default=1, max_length=5),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=12),
        ),
    ]
