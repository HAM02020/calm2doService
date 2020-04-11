from django.db import models


class TInfo(models.Model):
    user_id = models.IntegerField(primary_key=True)
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
        unique_together = (('pet_id', 'user'),)


class TTimes(models.Model):
    user = models.ForeignKey('TUser', models.DO_NOTHING)
    info_id = models.AutoField(primary_key=True)
    from_time = models.DateTimeField(blank=True, null=True)
    to_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_times'
        unique_together = (('info_id', 'user'),)


class TUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 't_user'
