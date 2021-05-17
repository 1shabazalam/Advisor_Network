from django.db.models import fields
from rest_framework import serializers
from .models import Advisors,Bookings, User
from users import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        extra_kwargs= {
            'password' : {'write_only': True}   
        }

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisors
        fields = ('id','name','profile_pic')

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ('id','booking_time','advisor','user')
        depth = 1


