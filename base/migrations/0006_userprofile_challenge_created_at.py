# Generated by Django 4.2.4 on 2023-08-11 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_remove_userprofile_challenge_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='challenge_created_at',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]