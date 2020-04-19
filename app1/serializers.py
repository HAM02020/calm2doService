from .models import *
from rest_framework import serializers

class TUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = TUser
        fields = ("__all__")

class PetSerializers(serializers.ModelSerializer):
    class Meta:
        model = TPet
        fields = ("__all__")
        extra_kwargs = {
            'pet_type': {
                'required': True,
                'help_text': '宠物类型型'
            }
        }

class TokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ("__all__")