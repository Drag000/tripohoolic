# Generated by Django 4.2.4 on 2023-08-13 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0013_alter_trips_used_agency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trips',
            name='used_agency',
            field=models.CharField(blank=True, choices=[('Shanotur', 'Shanotur'), ('Denita', 'Denita'), ('None', 'None')], max_length=30, null=True),
        ),
    ]
