# Generated by Django 4.2.17 on 2025-03-24 23:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Awards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('population', models.IntegerField(null=True)),
                ('actual_city_name', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('position', models.CharField(max_length=10)),
                ('height_in', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)])),
                ('weight', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)])),
                ('dob', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('active_team', models.BooleanField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.city')),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.franchise')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_game', models.DateField()),
                ('last_game', models.DateField(null=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.team')),
            ],
            options={
                'unique_together': {('player', 'team')},
            },
        ),
        migrations.CreateModel(
            name='PlayerGameScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_points', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)])),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerAward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1950), django.core.validators.MaxValueValidator(2100)])),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.awards')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.player')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='teams',
            field=models.ManyToManyField(related_name='players', through='data.PlayerTeam', to='data.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away', to='data.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home', to='data.team'),
        ),
    ]
