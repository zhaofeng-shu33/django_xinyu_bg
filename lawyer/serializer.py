from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from .models import Lawyer
class LawyerDetailSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(many=False)
    class Meta:
        model = Lawyer
        fields = ('user', 'law_firm')