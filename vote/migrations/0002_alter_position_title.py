# Generated by Django 4.1.5 on 2023-05-18 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
