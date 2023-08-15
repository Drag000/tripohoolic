# Generated by Django 4.2.4 on 2023-08-09 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_trips_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trips',
            name='type',
            field=models.CharField(choices=[('Solo', 'Solo'), ('Group', 'Group'), ('Agency', 'Agency')], max_length=6, verbose_name='Trip type'),
        ),
    ]
