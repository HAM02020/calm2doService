from datetime import datetime

from django.db import models

class TInfo(models.Model):
    user = models.ForeignKey('TUser', on_delete=models.CASCADE)
    finish_count = models.PositiveIntegerField(blank=True, null=True)
    interrupt_count = models.IntegerField(blank=True, null=True)
    duration = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_info'


class TPet(models.Model):
    user = models.ForeignKey('TUser', on_delete=models.CASCADE,help_text='用户id')
    pet_id = models.AutoField(primary_key=True)
    pet_name = models.CharField(max_length=255, blank=True, null=True,help_text='宠物名称')
    pet_type = models.CharField(max_length=20,help_text='宠物类型')

    class Meta:
        managed = True
        db_table = 't_pet'


class TTimes(models.Model):
    user = models.ForeignKey('TUser', on_delete=models.CASCADE)
    info_id = models.AutoField(primary_key=True)
    from_time = models.DateTimeField(blank=True, null=True)
    to_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_times'


class TUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.EmailField(max_length=50)
    user_name = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)

    nick_name = models.CharField(max_length=50,blank=True, null=True)
    join_time = models.DateTimeField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_user'

class Friend(models.Model):
    user = models.ForeignKey('TUser',on_delete=models.CASCADE)
    firend_id = models.IntegerField(max_length=11)
    remark_name = models.CharField(max_length=50,blank=True, null=True)
    class Meta:
        managed = True
        db_table = 't_friend'


class UserToken(models.Model):
    user = models.ForeignKey('TUser',on_delete=models.CASCADE)
    token = models.CharField(max_length=128)

    class Meta:
        managed = True
        db_table = 't_user_token'

