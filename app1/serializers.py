from .models import *
from rest_framework import serializers

class TUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = TUser
        fields = ("__all__")