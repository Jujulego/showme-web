# Generated by Django 2.0.2 on 2018-02-12 15:47

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_horaire'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('nom', models.CharField(blank=True, db_index=True, default='Inconnu', max_length=255)),
                ('telephone', models.CharField(blank=True, default='', max_length=20, verbose_name='téléphone')),
                ('note', models.FloatField(blank=True, null=True)),
                ('site', models.URLField(blank=True, max_length=500, null=True)),
                ('prix', models.SmallIntegerField(blank=True, choices=[(None, '----------'), (0, 'Gratuit'), (1, 'Bon marché'), (2, 'Modéré'), (3, 'Cher'), (4, 'Très cher')], default=None)),
                ('photo', models.ImageField(blank=True, max_length=500, null=True, upload_to='photos/')),
            ],
            options={
                'verbose_name_plural': 'lieux',
            },
        ),
    ]
