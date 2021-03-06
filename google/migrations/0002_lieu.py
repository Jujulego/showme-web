# Generated by Django 2.0.2 on 2018-02-14 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_lieu_adresse'),
        ('google', '0001_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_id', models.CharField(db_index=True, editable=False, max_length=255, unique=True)),
                ('maj', models.BooleanField(default=False)),
                ('der_maj', models.DateField(auto_now_add=True)),
                ('lieu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='api.Lieu')),
            ],
            options={
                'verbose_name_plural': 'lieux',
            },
        ),
    ]
