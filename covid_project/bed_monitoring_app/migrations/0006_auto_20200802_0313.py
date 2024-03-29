# Generated by Django 3.0.3 on 2020-08-02 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bed_monitoring_app', '0005_userprofileinfo_phone_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalbeddetails',
            name='occupied_beds_under_scheme',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='hospitalbeddetails',
            name='occupied_o2_beds',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='hospitalbeddetails',
            name='occupied_ventilator_beds',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='hospitalbeddetails',
            name='total_beds_under_scheme',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='hospitalbeddetails',
            name='total_o2_beds',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospitalbeddetails',
            name='total_ventilator_beds',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='address',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='hospital_name',
            field=models.CharField(max_length=100),
        ),
    ]
