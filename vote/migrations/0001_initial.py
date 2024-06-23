# Generated by Django 5.0.6 on 2024-06-18 22:32

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Position Title')),
            ],
            options={
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positions',
            },
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('max_voters', models.IntegerField()),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('commissioner_token', models.CharField(default=None, max_length=50, unique=True)),
                ('commissioner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elections', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('about', models.TextField(blank=True, default='No additional information.', verbose_name='About the Candidate')),
                ('total_vote', models.IntegerField(default=0, editable=False)),
                ('party', models.CharField(choices=[('up', 'Unity Party'), ('lp', 'Liberty Party'), ('anc', 'Alternative National Congress'), ('cdc', 'Coalition for Democratic Change'), ('pup', 'People’s Unification Party'), ('alp', 'All Liberian Party'), ('movee', 'Movement for Economic Empowerment'), ('mdr', 'Movement for Democracy and Reconstruction'), ('rainbow', 'Rainbow Alliance'), ('volt', 'Vision for Liberia Transformation'), ('sup', 'Students Unification Party'), ('prosa', 'Progressive Student Alliance'), ('sim', 'Student Integration Movement'), ('stud', 'Student Democratic Alliance')], default='Independent', max_length=50)),
                ('image', models.ImageField(upload_to='images/', verbose_name='Candidate Pic')),
                ('election', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='vote.election')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='vote.position')),
            ],
            options={
                'verbose_name': 'Candidate',
                'verbose_name_plural': 'Candidates',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default=None, max_length=30, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(default=None, max_length=30, null=True, verbose_name='Last Name')),
                ('university_name', models.CharField(blank=True, max_length=100, null=True)),
                ('high_school_name', models.CharField(blank=True, max_length=100, null=True)),
                ('level', models.CharField(blank=True, max_length=50, null=True)),
                ('major', models.CharField(blank=True, max_length=100, null=True)),
                ('student_id', models.CharField(blank=True, max_length=50, null=True)),
                ('district', models.CharField(max_length=50, verbose_name='District')),
                ('county', models.CharField(max_length=50, verbose_name='County')),
                ('citizenship', models.BooleanField(default=False, verbose_name='Has Citizenship')),
                ('age', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(120)], verbose_name='Age')),
                ('role', models.CharField(choices=[('commissioner', 'Election Commissioner'), ('voter', 'Voter')], default='voter', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter_id', models.CharField(max_length=50, unique=True)),
                ('can_vote', models.BooleanField(default=True)),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voters', to='vote.election')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ControlVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('party', models.CharField(default='Independent', max_length=50, verbose_name='Party')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='control_votes', to='vote.candidate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='control_votes', to=settings.AUTH_USER_MODEL)),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='control_votes', to='vote.election')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='control_votes', to='vote.position')),
            ],
            options={
                'verbose_name': 'Control Vote',
                'verbose_name_plural': 'Control Votes',
                'unique_together': {('user', 'election', 'position', 'candidate')},
            },
        ),
    ]
