# Generated by Django 5.0.6 on 2024-07-02 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_alter_position_title_alter_profile_role_observer'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='max_observers',
            field=models.IntegerField(default=0),
        ),
    ]
