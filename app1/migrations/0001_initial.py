# Generated by Django 3.0.5 on 2020-06-06 15:36

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
                ('user_email', models.EmailField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
                ('user_password', models.CharField(max_length=50)),
                ('nick_name', models.CharField(blank=True, max_length=50, null=True)),
                ('join_time', models.DateTimeField(blank=True, null=True)),
                ('birthday', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 't_user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.TUser')),
            ],
            options={
                'db_table': 't_user_token',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TTimes',
            fields=[
                ('time_id', models.AutoField(primary_key=True, serialize=False)),
                ('from_time', models.DateTimeField(blank=True, null=True)),
                ('to_time', models.DateTimeField(blank=True, null=True)),
                ('set_time', models.DateTimeField(blank=True, null=True)),
                ('is_finish', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.TUser')),
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
                ('pet_name', models.CharField(blank=True, help_text='宠物名称', max_length=255, null=True)),
                ('pet_type', models.CharField(help_text='宠物类型', max_length=20)),
                ('user', models.ForeignKey(help_text='用户id', on_delete=django.db.models.deletion.CASCADE, to='app1.TUser')),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.TUser')),
            ],
            options={
                'db_table': 't_info',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firend_id', models.IntegerField(blank=True, max_length=11, null=True)),
                ('remark_name', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.TUser')),
            ],
            options={
                'db_table': 't_friend',
                'managed': True,
            },
        ),
    ]
