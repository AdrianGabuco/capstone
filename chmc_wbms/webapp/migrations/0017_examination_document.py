# Generated by Django 5.0.1 on 2025-01-05 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_alter_examination_attending_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='examination',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='examination_documents/'),
        ),
    ]