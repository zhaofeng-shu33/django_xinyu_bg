from rest_auth.serializer import UserDetailsSerializer
class LawyerDetailSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()
    class Meta:
        model = Lawyer
