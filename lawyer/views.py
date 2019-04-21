from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .serializer import LawyerDetailSerializer
from .models import Lawyer
# Create your views here.
class LawyerDetailsView(RetrieveUpdateAPIView):
    serializer_class = LawyerDetailSerializer
    permission_classes = (IsAuthenticated, )
    def get_object(self):
        try:
            return Lawyer.objects.get(user=self.request.user)
        except Lawyer.DoesNotExist:
            raise NotFound('current user is not lawyer')