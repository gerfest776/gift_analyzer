# Generated by Django 4.0.1 on 2022-01-30 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Importer',
            fields=[
                ('import_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'importer',
            },
        ),
        migrations.CreateModel(
            name='Villager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizen_id', models.PositiveIntegerField(verbose_name='Паспортный номер')),
                ('town', models.CharField(max_length=30, verbose_name='Название города')),
                ('street', models.CharField(max_length=50, verbose_name='Улица')),
                ('building', models.CharField(max_length=50, verbose_name='Номер дома, корпус и строение')),
                ('apartment', models.PositiveSmallIntegerField(verbose_name='Номер квартиры')),
                ('name', models.CharField(max_length=50, verbose_name='Полное имя')),
                ('birth_date', models.DateField(verbose_name='Дата рождения в формате ДД.ММ.ГГГГ')),
                ('gender', models.CharField(max_length=6, verbose_name='Гендер')),
                ('importer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='villagers', to='villagers.importer')),
                ('relatives', models.ManyToManyField(to='villagers.Villager')),
            ],
            options={
                'db_table': 'villager',
            },
        ),
    ]