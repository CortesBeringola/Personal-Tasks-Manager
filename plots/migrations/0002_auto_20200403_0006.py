# Generated by Django 2.2.4 on 2020-04-03 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]
