# Generated by Django 4.0.2 on 2022-02-18 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zomatoApp', '0009_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='status',
        ),
    ]
