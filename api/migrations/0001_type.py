# Generated by Django 2.0.2 on 2018-02-12 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('pluriel', models.CharField(max_length=100)),
                ('blacklist', models.BooleanField(default=False)),
            ],
        ),
    ]
