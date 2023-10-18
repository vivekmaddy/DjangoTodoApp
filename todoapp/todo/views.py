from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination



from .models import *
from .serializers import *


status_code_text = {
    200 : 'Ok',
}


class TodoListViewset(ModelViewSet):
    """TodoList viewset for CRUD"""
    queryset = TodoLists.objects.all().order_by('-id')
    serializer_class = TodoListSerializer
    pagination_class = PageNumberPagination


    def list(self, request):
        status_code = HTTP_200_OK
        response = {
            'message' : status_code_text[200],
            'status' : status_code,
            'data' : {} 
        }
        try:
            qs = self.get_queryset()
            paginator = self.pagination_class()
            paginator.page_size = request.GET.get("limit", 5)
            result_page = paginator.paginate_queryset(qs, request) 
            result = self.get_serializer(result_page, many=True)
            response["data"] = paginator.get_paginated_response(result.data).data

        except Exception as err:
            response['message'] = str(err)
            response['status'] = status_code = HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)
    

    def partial_update(self, request, pk=None):
        status_code = HTTP_200_OK
        response = {
            'message' : "Updated!",
            'status' : status_code,
            'data' : {} 
        }

        try:
            serializer = TodoCreateUpdateSerializer(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            data["status"] = self.get_object().get_status_display()
            response["data"] = data
        except Exception as err:
            response['message'] = str(err)
            response['status'] = status_code = HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)
    

    def destroy(self, request, pk=None):
        status_code = HTTP_200_OK
        response = {
            'message' : "Deleted!",
            'status' : status_code,
            'data' : {} 
        }

        try:
            instance = self.get_object()
            instance.delete()
        except Exception as err:
            response['message'] = str(err)
            response['status'] = status_code = HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)
    
    
    def create(self, request):
        status_code = HTTP_200_OK
        response = {
            'message' : status_code_text[status_code],
            'status' : status_code,
            'data' : {} 
        }
        try:
            serializer = TodoCreateUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response["data"] = serializer.data
        except Exception as err:
            response['message'] = str(err)
            response['status'] = status_code = HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)