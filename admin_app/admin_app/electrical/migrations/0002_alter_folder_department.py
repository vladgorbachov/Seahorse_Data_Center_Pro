# Generated by Django 5.0.6 on 2024-08-18 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electrical', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='department',
            field=models.CharField(choices=[('deck', 'Deck'), ('bridge', 'Bridge'), ('catering', 'Catering'), ('electrical', 'Electrical'), ('engine', 'Engine')], default='deck', max_length=10),
        ),
    ]
