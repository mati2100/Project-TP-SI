from django.db import models
import random
import string
from datetime import timedelta
from django.utils import timezone

# Create your models here.

class Agent(models.Model):
    agent_name=models.CharField(max_length=50)
    agent_email=models.EmailField()
    agent_pwd=models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.agent_name+" ("+self.agent_email+")"
    
class PasswordResetCode(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        # Le code est valide pendant 5 minutes
        expiration_time = self.created_at + timedelta(minutes=5)
        return not self.is_used and timezone.now() < expiration_time
    
    @classmethod
    def generate_code(cls):
        return ''.join(random.choices(string.digits, k=6))