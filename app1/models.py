from django.db import models

class TInfo(models.Model):
    user = models.ForeignKey('TUser', models.DO_NOTHING)
    finish_count = models.PositiveIntegerField(blank=True, null=True)
    interrupt_count = models.IntegerField(blank=True, null=True)
    duration = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_info'


class TPet(models.Model):
    user = models.ForeignKey('TUser', models.DO_NOTHING)
    pet_id = models.AutoField(primary_key=True)
    pet_name = models.CharField(max_length=255, blank=True, null=True)
    pet_type = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_pet'


class TTimes(models.Model):
    user = models.ForeignKey('TUser', models.DO_NOTHING)
    info_id = models.AutoField(primary_key=True)
    from_time = models.DateTimeField(blank=True, null=True)
    to_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_times'


class TUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 't_user'

class UserToken(models.Model):
    token_id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=128)
    user = models.OneToOneField(to="TUser",on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 't_user_token'

