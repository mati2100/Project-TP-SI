from django.db import models
import random
import string
from datetime import timedelta
from django.utils import timezone
import uuid
from django.db import models


# Create your models here.

class Agent(models.Model):
    agent_first_name=models.CharField(max_length=50)
    agent_last_name=models.CharField(max_length=50)
    agent_email=models.EmailField(verbose_name="Adresse email",unique=True)

    agent_username=models.CharField(max_length=50, unique=True)
    agent_password_hash=models.CharField(max_length=128)

    acount_status_choices = [('active', 'Active'), ('inactive', 'Inactive'), ('suspended', 'Suspended')]
    agent_account_status = models.CharField(max_length=20, choices=acount_status_choices, default='active')

    agent_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agent_first_name + " " + self.agent_last_name + " (" + self.agent_email + ")"
    
    #untouched classes below
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

class AgentToken(models.Model):
    agent = models.OneToOneField(
        'Agent',
        on_delete=models.CASCADE,
        related_name='token'
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agent.agent_first_name} {self.agent.agent_last_name}"    