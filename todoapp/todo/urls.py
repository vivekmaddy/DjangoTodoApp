from django.urls import path, include
from rest_framework import routers

from .views import TodoListViewset, UserSignUpViewset, UserLoginViewset

router = routers.DefaultRouter()
router.register(r'todolist', TodoListViewset)

auth_router = routers.DefaultRouter()
auth_router.register(r'signup', UserSignUpViewset)
auth_router.register(r'login', UserLoginViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('user/', include(auth_router.urls)),
]