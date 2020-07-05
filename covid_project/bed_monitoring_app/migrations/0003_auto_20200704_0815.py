# Generated by Django 3.0.3 on 2020-07-04 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bed_monitoring_app', '0002_hospitalbeddetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalbeddetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]