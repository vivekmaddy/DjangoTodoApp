from django.contrib import admin
from .models import *
# Register your models here.

class TodoListsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'status')

admin.site.register(TodoLists, TodoListsAdmin)
