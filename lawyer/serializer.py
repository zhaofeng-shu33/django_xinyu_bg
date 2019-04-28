from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from rest_framework.fields import empty
from .models import Lawyer, Class, Course
from rest_framework.exceptions import PermissionDenied
import pdb

class LawyerClassViewSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    course_2 = serializers.StringRelatedField()
    class Meta:
        model = Class
        fields = ('pk','school','start_time', 'course', 'grade', 'class_id', 'start_time_2', 'course_2')

class LawyerDetailSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(many=False, required=False)
    lawyer_classes = LawyerClassViewSerializer(many=True)
    class Meta:
        model = Lawyer
        fields = ('user', 'law_firm', 'lawyer_classes')
    def update(self, instance, validated_data):
        user_data = validated_data.get('user', None)
        if(user_data):
            user = instance.user
            for k,v in user_data.items():
                setattr(user, k, v)
            user.save()
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
class LawyerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ('user',)
        
class ClassViewSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    lawyer = LawyerViewSerializer()
    course = serializers.StringRelatedField()
    course_2 = serializers.StringRelatedField()
    class Meta:
        model = Class
        fields = ('pk','school','lawyer','start_time', 'course', 'grade', 'class_id', 'start_time_2', 'course_2')
        
class ClassApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('lawyer',)
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if(instance.lawyer):
            if(instance.lawyer.user != user):
                raise PermissionDenied("cannot cancel other's apply")
            else:
                instance.lawyer = None
        else:
            try:
                p = Lawyer.objects.get(user=user)
            except Lawyer.DoesNotExist:
                p = Lawyer(user=user)
                p.save()
            instance.lawyer = p
        instance.save()
        return instance
