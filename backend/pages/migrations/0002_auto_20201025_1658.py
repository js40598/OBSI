# Generated by Django 3.1.2 on 2020-10-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='date',
            new_name='datetime',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='places',
            new_name='number_of_places',
        ),
        migrations.AddField(
            model_name='reservation',
            name='is_upcoming',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='availability_level',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
