# Generated by Django 4.2.4 on 2023-08-09 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trips', '0005_trips_notes_trips_transport'),
    ]

    operations = [
        migrations.AddField(
            model_name='trips',
            name='publication_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='trips',
            name='user',
            field=models.ForeignKey(default=2232, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
