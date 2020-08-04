# Generated by Django 3.0.3 on 2020-08-03 11:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bed_monitoring_app', '0007_auto_20200803_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalbeddetails',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospitalbeddetails',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
