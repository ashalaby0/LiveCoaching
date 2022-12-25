from rest_framework import serializers

from . import models
class CoachSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    speciality = serializers.ReadOnlyField(source='speciality.name')
    # speciality = serializers.ReadOnlyField(source='Category.name')

    class Meta:
        model = models.Coach
        fields = '__all__'


class CustomerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerMessage
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = '__all__'