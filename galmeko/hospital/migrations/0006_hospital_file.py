# Generated by Django 3.0.2 on 2020-01-28 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_remove_hospital_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to='hospital/'),
        ),
    ]
