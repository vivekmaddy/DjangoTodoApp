from django.urls import path, include
from rest_framework import routers

from .views import TodoListViewset

router = routers.DefaultRouter()
router.register(r'todolist', TodoListViewset)

urlpatterns = [
    path('', include(router.urls)),
]