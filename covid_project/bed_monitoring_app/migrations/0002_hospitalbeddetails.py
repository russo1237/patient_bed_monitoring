# Generated by Django 3.0.3 on 2020-07-04 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bed_monitoring_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalBedDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_no_of_beds', models.IntegerField()),
                ('total_govt_beds', models.IntegerField()),
                ('total_hospital_beds', models.IntegerField()),
                ('occupied_govt_beds', models.IntegerField(default=0)),
                ('occupied_hospital_beds', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
