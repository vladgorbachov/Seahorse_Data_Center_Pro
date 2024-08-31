# Generated by Django 5.0.6 on 2024-08-18 20:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DPHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('hours', models.IntegerField()),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('link', models.CharField(blank=True, max_length=2048, null=True)),
                ('is_local_link', models.BooleanField(default=False)),
                ('visible', models.BooleanField(default=True)),
                ('is_file', models.BooleanField(default=False)),
                ('department', models.CharField(choices=[('deck', 'Deck'), ('bridge', 'Bridge')], default='deck', max_length=10)),
                ('parent_folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subfolders', to='bridge.folder')),
            ],
        ),
        migrations.CreateModel(
            name='FileMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(blank=True, max_length=50, null=True)),
                ('size', models.BigIntegerField(default=0)),
                ('last_modified', models.DateTimeField(blank=True, null=True)),
                ('icon_path', models.CharField(blank=True, max_length=255, null=True)),
                ('folder', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='metadata', to='bridge.folder')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rows', models.IntegerField()),
                ('columns', models.IntegerField()),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='bridge.folder')),
            ],
        ),
        migrations.CreateModel(
            name='TableCell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField()),
                ('column', models.IntegerField()),
                ('content', models.TextField(blank=True)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cells', to='bridge.table')),
            ],
        ),
    ]
