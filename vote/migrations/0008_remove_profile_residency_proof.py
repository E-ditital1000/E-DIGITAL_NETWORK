# Generated by Django 4.2.1 on 2023-05-27 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0007_alter_profile_citizenship_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='residency_proof',
        ),
    ]