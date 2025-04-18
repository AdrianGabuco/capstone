# Generated by Django 5.0.1 on 2024-12-12 17:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0014_patient_examination_patient_payment_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='patient',
        ),
        migrations.AddField(
            model_name='payment',
            name='examination',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='webapp.examination'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending', max_length=100),
        ),
    ]
