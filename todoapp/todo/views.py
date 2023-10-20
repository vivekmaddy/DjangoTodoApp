from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from .serializers import *



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


status_code_text = {
    200 : 'Ok',
}



from rest_framework.permissions import IsAuthenticated

class TodoListViewset(ModelViewSet):
    """TodoList viewset for CRUD"""
    queryset = TodoLists.objects.all().order_by('-id')
    serializer_class = TodoListSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    


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
            payload = request.data
            payload["user"] = request.user.id
            serializer = TodoCreateUpdateSerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response["data"] = serializer.data
        except Exception as err:
            response['message'] = str(err)
            response['status'] = status_code = HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)
    


class UserSignUpViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserAuthModelSerializer
    permission_classes = []


    def create(self, request):
        status_code = HTTP_200_OK
        response = {
            'message' : status_code_text[status_code],
            'status' : status_code,
            'data' : {} 
        }
        try:
            payload = request.data
            if payload["password"] != payload["repassword"]:
                raise Exception("Passwords are not matching")
            
            payload["email"] = payload["username"]
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                err_string = ""
                errors_dict = serializer.errors
                for error in errors_dict.keys():
                    err_string += f"{errors_dict[error][0]}"
                raise Exception(err_string)
            
            serializer.save()
        except Exception as err:
            response['message'] = str(err)
            response['status'] = status_code = HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)




class UserLoginViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()

    def create(self, request):
        status_code = HTTP_200_OK
        response = {
            'message' : status_code_text[status_code],
            'status' : status_code,
            'data' : {} 
        }
        try:
            payload = request.data
            username, password = payload["username"], payload["password"]
            user = authenticate(username=username, password=password)

            if user is None:
                raise Exception("Invalid username or password")
            token_data = get_tokens_for_user(user)
            response["data"].update(token_data)
        except Exception as err:
            response['message'] = str(err)
            response['status'] = status_code = HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)
    

