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

class LawyerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ('user',)

class LectureSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    lawyer = LawyerViewSerializer()
    class Meta:
        model = Lecture
        fields = ('course', 'start_time', 'duration', 'lawyer')

class LawyerLectureClassSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    class Meta:
        model = Class
        fields = ('pk', 'school', 'grade', 'class_id')

class LawyerLectureSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    classroom = LawyerLectureClassSerializer()
    class Meta:
        model = Lecture
        fields = ('course', 'start_time', 'duration', 'classroom')
        
class LawyerClassViewSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    lectures = LectureSerializer(many=True)
    class Meta:
        model = Class
        fields = ('pk', 'school', 'grade', 'class_id', 'lectures')

class LawyerDetailGetSerialier(serializers.ModelSerializer):
    user = UserDetailsSerializer(many=False)
    lawyer_lectures = LawyerLectureSerializer(many=True)
    class Meta:
        model = Lawyer
        fields = ('user', 'lawyer_lectures')
    def to_representation(self, instance):
        """instance is an Lawyer"""
        ret = super().to_representation(instance)
        office = instance.get_current_office()
        ret['office'] = LawyerOfficeSerializer(office).data
        return ret
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




class ClassViewSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    lectures = LectureSerializer(many=True)
    class Meta:
        model = Class
        fields = ('pk','school', 'grade', 'class_id', 'lectures')
        
# for lawyer applies and cancel lectures
def apply_or_cancel_lectures(request, classroom):
    user = request.user
    # get the first class lawyer
    first_lecture = classroom.lectures.all()[0]
    lawyer_id = -1
    if(first_lecture.lawyer):
        if(first_lecture.lawyer.user != user):
            raise PermissionDenied("cannot cancel other's apply")
        else:
            classroom.lectures.update(lawyer = None)
    else:
        try:
            p = Lawyer.objects.get(user=user)
        except Lawyer.DoesNotExist:
            p = Lawyer(user=user)
            p.save()
        lawyer_id = p.id
        classroom.lectures.update(lawyer = p) # bulk update
    return lawyer_id

