# Generated by Django 4.0.2 on 2022-02-18 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zomatoApp', '0011_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
