from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .serializer import LawyerOfficeSerializer, ClassViewSerializer, ClassApplySerializer,\
    LawyerDetailGetSerialier, LawyerDetailPutSerializer
from .models import Lawyer, LawyerOffice, Class

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

class LawyerDetailsView(APIView):
    permission_classes = (IsAuthenticated, )
    def get_object(self):
        try:
            return Lawyer.objects.get(user=self.request.user)
        except Lawyer.DoesNotExist:
            p = Lawyer(user=self.request.user)
            p.save()
            return p
    def get(self, request, format=None):
        p = self.get_object()
        serializer = LawyerDetailGetSerialier(p)
        return Response(serializer.data)
    def put(self, request, format=None):
        p = self.get_object()
        serializer = LawyerDetailPutSerializer(p, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer_2 = LawyerDetailGetSerialier(p)
            return Response(serializer_2.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
class ClassListView(ListAPIView):
    queryset = Class.objects.order_by('lawyer')
    pagination_class = StandardResultsSetPagination
    serializer_class = ClassViewSerializer
    
class ClassRegisterView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Class.objects.all()
    serializer_class = ClassApplySerializer

class LawyerOfficeView(ListAPIView):
    queryset = LawyerOffice.objects.all()
    serializer_class = LawyerOfficeSerializer