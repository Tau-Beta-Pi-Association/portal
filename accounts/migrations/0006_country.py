# Generated by Django 5.0.6 on 2024-07-15 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_code', models.CharField(max_length=3)),
                ('phone_code', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
    ]
