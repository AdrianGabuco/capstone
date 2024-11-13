# Generated by Django 5.0.1 on 2024-11-12 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_alter_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='account_type',
            field=models.CharField(blank=True, choices=[('admin', 'Admin'), ('employee', 'Employee'), ('doctor', 'Doctor')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]