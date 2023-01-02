from rest_framework import serializers

from . import models
class CoachSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
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

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PromoCode
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Certificate
        fields = '__all__'