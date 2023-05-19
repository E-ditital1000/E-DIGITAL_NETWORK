# Generated by Django 4.1.5 on 2023-05-19 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0005_candidate_county_candidate_district_candidate_party'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('national_id', models.CharField(max_length=50)),
                ('citizenship', models.BooleanField()),
                ('age', models.IntegerField()),
                ('residency_proof', models.FileField(upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
