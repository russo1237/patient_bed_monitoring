# Generated by Django 3.0.3 on 2020-08-03 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bed_monitoring_app', '0006_auto_20200802_0313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospitalbeddetails',
            old_name='occupied_ventilator_beds',
            new_name='occupied_icu_beds',
        ),
        migrations.RenameField(
            model_name='hospitalbeddetails',
            old_name='total_ventilator_beds',
            new_name='total_icu_beds',
        ),
        migrations.AddField(
            model_name='hospitalbeddetails',
            name='occupied_icu_ventilator_beds',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='hospitalbeddetails',
            name='total_icu_ventilator_beds',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hospitalbeddetails',
            name='total_beds_under_scheme',
            field=models.IntegerField(),
        ),
    ]
