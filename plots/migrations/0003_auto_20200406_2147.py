# Generated by Django 2.2.4 on 2020-04-06 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0002_auto_20200403_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='month',
            field=models.CharField(choices=[('Jan', 'Jan'), ('Feb', 'Feb'), ('Mar', 'Mar'), ('Apr', 'Apr'), ('May', 'May'), ('Jun', 'Jun'), ('Jul', 'Jul'), ('Aug', 'Aug'), ('Sep', 'Sep'), ('Oct', 'Oct'), ('Nov', 'Nov'), ('Dec', 'Dec')], max_length=3),
        ),
    ]
