# Generated by Django 5.0.1 on 2024-11-17 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_alter_customuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='prefix',
            field=models.CharField(blank=True, choices=[('', 'No Prefix'), ('Dr.', 'Dr.'), ('Dra.', 'Dra.')], max_length=10, null=True),
        ),
    ]
