# Generated by Django 3.0.3 on 2020-07-14 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bed_monitoring_app', '0003_auto_20200704_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='address',
            field=models.TextField(max_length=70),
        ),
    ]