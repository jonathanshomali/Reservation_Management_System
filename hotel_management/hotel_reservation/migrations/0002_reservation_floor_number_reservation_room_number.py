# Generated by Django 4.2 on 2023-05-02 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='floor_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='room_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
