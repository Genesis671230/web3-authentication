# Generated by Django 4.2.4 on 2023-08-11 08:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_userprofile_challenge_expiration'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='challenge_created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 11, 8, 2, 17, 803662, tzinfo=datetime.timezone.utc)),
        ),
    ]
