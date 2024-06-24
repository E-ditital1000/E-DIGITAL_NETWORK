# Generated by Django 5.0.6 on 2024-06-24 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='party',
            field=models.CharField(choices=[('up', 'Unity Party'), ('lp', 'Liberty Party'), ('anc', 'Alternative National Congress'), ('cdc', 'Coalition for Democratic Change'), ('pup', 'People’s Unification Party'), ('alp', 'All Liberian Party'), ('movee', 'Movement for Economic Empowerment'), ('mdr', 'Movement for Democracy and Reconstruction'), ('rainbow', 'Rainbow Alliance'), ('volt', 'Vision for Liberia Transformation'), ('SUP', 'Students Unification Party'), ('PROSA', 'Progressive Student Alliance'), ('SIM', 'Mighty Student Integration Movement'), ('STUD', 'Student Democratic Alliance')], default='Independent', max_length=50),
        ),
    ]