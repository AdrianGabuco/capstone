# Generated by Django 5.0.1 on 2024-11-17 17:58

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_servicetype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patient',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='appointment',
            name='client_name',
            field=models.CharField(default='Client', max_length=100),
        ),
        migrations.AddField(
            model_name='appointment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AppointmentServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.appointment')),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.servicetype')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='service_types',
            field=models.ManyToManyField(through='webapp.AppointmentServiceType', to='webapp.servicetype'),
        ),
    ]
