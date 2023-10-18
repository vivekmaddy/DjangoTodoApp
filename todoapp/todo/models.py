from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class TodoLists(Base):
    status_choices = (
        (1, "Todo"),
        (2, "In progress"),
        (3, "Completed"),
        (4, "Rescheduled"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    scheduled_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=status_choices, default=1)

    def __str__(self) -> str:
        return self.title

