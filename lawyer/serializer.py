from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from rest_framework.fields import empty
from .models import Lawyer
import pdb
class LawyerDetailSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(many=False, required=False)
    class Meta:
        model = Lawyer
        fields = ('user', 'law_firm')
    def update(self, instance, validated_data):
        user_data = validated_data.get('user', None)
        if(user_data):
            user = instance.user
            for k,v in user_data.items():
                setattr(user, k, v)
        for k,v in validated_data.items():
            if(k == 'user'):
                continue
            setattr(instance, k, v)
        instance.save()
        return instance
    def run_validation(self, data=empty):
        # self the instance for UserSerializer
        self.fields['user'].instance = self.instance.user
        return super(LawyerDetailSerializer, self).run_validation(data=data)