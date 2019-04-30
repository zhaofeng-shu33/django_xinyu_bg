from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import empty
from .models import LawyerOffice, Lawyer, Class, Course, Lecture
from rest_framework.exceptions import PermissionDenied

class LawyerOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerOffice
        fields = '__all__'

# Get the UserModel
UserModel = get_user_model()

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email')

class LawyerClassViewSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    course_2 = serializers.StringRelatedField()
    class Meta:
        model = Class
        fields = ('pk', 'school', 'start_time', 'course', 'grade', 'class_id', 'start_time_2', 'course_2')

class LawyerDetailGetSerialier(serializers.ModelSerializer):
    user = UserDetailsSerializer(many=False)
    lawyer_classes = LawyerClassViewSerializer(many=True)
    office = LawyerOfficeSerializer()
    class Meta:
        model = Lawyer
        fields = ('user', 'lawyer_classes', 'office')

class LawyerDetailPutSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(many=False, required=False)
    class Meta:
        model = Lawyer
        fields = ('user', 'office')
    def update(self, instance, validated_data):
        user_data = validated_data.get('user', None)
        if(user_data):
            user = instance.user
            for k,v in user_data.items():
                setattr(user, k, v)
            user.save()
        if(validated_data.get('office', None)):
            instance.office = validated_data['office'];
        for k,v in validated_data.items():
            if(k == 'user' or k == 'office'):
                continue
            setattr(instance, k, v)
        instance.save()
        return instance
    def run_validation(self, data=empty):
        # self the instance for UserSerializer
        self.fields['user'].instance = self.instance.user
        return super(LawyerDetailPutSerializer, self).run_validation(data=data)

class LawyerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ('user',)

class LectureSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    class Meta:
        model = Lecture
        fields = ('course', 'start_time', 'duration')
        
class ClassViewSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    lawyer = LawyerViewSerializer()
    course = serializers.StringRelatedField()
    course_2 = serializers.StringRelatedField()
    lectures = LectureSerializer(many=True)
    class Meta:
        model = Class
        fields = ('pk','school','lawyer','start_time', 'course', 'grade', 'class_id', 'start_time_2', 'course_2', 'lectures')
        
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

