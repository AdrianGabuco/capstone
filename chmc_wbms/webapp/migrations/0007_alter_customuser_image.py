# Generated by Django 5.0.1 on 2024-11-13 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_remove_customuser_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, default='static/image/profile_ICON.png', null=True, upload_to='profile_pics/'),
        ),
    ]
