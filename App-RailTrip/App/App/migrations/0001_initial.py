# Generated by Django 5.1.1 on 2024-12-18 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mdp', models.CharField(max_length=128)),
                ('pseudo', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoadTrip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nom du voyage')),
                ('description', models.TextField(max_length=500, verbose_name='Description du voyage')),
                ('publique', models.BooleanField(default=False, verbose_name='Voyage public')),
                ('depart', models.DateTimeField(verbose_name='Date de départ')),
                ('retour', models.DateTimeField(blank=True, null=True, verbose_name='Date de retour')),
                ('nbjour', models.PositiveIntegerField(default=1, verbose_name='Nombre de jours')),
                ('etapes', models.JSONField(default=list, verbose_name='Étapes du voyage')),
                ('prix_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Prix total')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roadtrips', to='App.utilisateur', verbose_name='Voyageur')),
            ],
            options={
                'verbose_name': 'Road Trip',
                'verbose_name_plural': 'Road Trips',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('like', models.BooleanField(default=False)),
                ('roadtrip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.roadtrip')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Favori',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('roadtrip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.roadtrip')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.utilisateur')),
            ],
        ),
    ]
