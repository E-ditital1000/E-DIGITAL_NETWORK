# Generated by Django 4.1.5 on 2023-05-18 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_controlvote_county_controlvote_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='controlvote',
            name='party',
            field=models.CharField(default='Unknown', max_length=50),
        ),
    ]
