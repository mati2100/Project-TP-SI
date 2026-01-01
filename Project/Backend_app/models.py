from django.db import models

# Create your models here.

class Agent(models.Model):
    agent_name=models.CharField(max_length=50)
    agent_email=models.EmailField()
    agent_pwd=models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.agent_name+" ("+self.role+")"