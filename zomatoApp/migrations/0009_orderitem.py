# Generated by Django 4.0.2 on 2022-02-16 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zomatoApp', '0008_remove_seat_booking_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_price', models.FloatField()),
                ('qty', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zomatoApp.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zomatoApp.order')),
            ],
        ),
    ]
