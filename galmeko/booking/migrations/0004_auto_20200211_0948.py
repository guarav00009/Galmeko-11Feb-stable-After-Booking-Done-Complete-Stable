# Generated by Django 3.0.2 on 2020-02-11 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_auto_20200211_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='destination_geocode',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Destination Cordinate'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='origin_geocode',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Origin Cordinate'),
        ),
    ]
