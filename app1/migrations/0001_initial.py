# Generated by Django 3.0.5 on 2020-04-11 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TUser',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=255)),
                ('user_password', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 't_user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TTimes',
            fields=[
                ('info_id', models.AutoField(primary_key=True, serialize=False)),
                ('from_time', models.DateTimeField(blank=True, null=True)),
                ('to_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app1.TUser')),
            ],
            options={
                'db_table': 't_times',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TPet',
            fields=[
                ('pet_id', models.AutoField(primary_key=True, serialize=False)),
                ('pet_name', models.CharField(blank=True, max_length=255, null=True)),
                ('pet_type', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app1.TUser')),
            ],
            options={
                'db_table': 't_pet',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finish_count', models.PositiveIntegerField(blank=True, null=True)),
                ('interrupt_count', models.IntegerField(blank=True, null=True)),
                ('duration', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app1.TUser')),
            ],
            options={
                'db_table': 't_info',
                'managed': True,
            },
        ),
    ]
