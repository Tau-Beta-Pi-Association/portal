# Generated by Django 5.0.6 on 2024-07-01 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
