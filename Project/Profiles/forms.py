from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import Agent
import re

class LoginForm(forms.Form):
    agent_username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    agent_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('agent_username')
        password = cleaned_data.get('agent_password')
        
        if username and password:
            try:
                agent = Agent.objects.get(agent_username=username)
                # Verify password hash
                if not check_password(password, agent.agent_password_hash):
                    raise forms.ValidationError("Invalid username or password")
                    
                # Check if account is active
                if agent.agent_account_status != 'active':
                    raise forms.ValidationError("Your account is not active. Please contact administrator.")
                    
            except Agent.DoesNotExist:
                raise forms.ValidationError("Invalid username or password")
                
        return cleaned_data

class AddAgentForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )
    
    class Meta:
        model = Agent
        fields = ['agent_first_name', 'agent_last_name', 'agent_email', 'agent_username']
        widgets = {
            'agent_first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'agent_last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'agent_email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'agent_username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
        )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        # Password strength validation
        if password:
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("Password must contain at least one uppercase letter")
            if not re.search(r'[a-z]', password):
                raise forms.ValidationError("Password must contain at least one lowercase letter")
            if not re.search(r'[0-9]', password):
                raise forms.ValidationError("Password must contain at least one number")
        
        # Check unique constraints
        email = cleaned_data.get('agent_email')
        username = cleaned_data.get('agent_username')
        
        if email and Agent.objects.filter(agent_email=email).exists():
            if not self.instance.pk:  # Only check for new agents
                raise forms.ValidationError("An agent with this email already exists")
        
        if username and Agent.objects.filter(agent_username=username).exists():
            if not self.instance.pk:  # Only check for new agents
                raise forms.ValidationError("An agent with this username already exists")
        
        return cleaned_data
    
    def save(self, commit=True):
        agent = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        if password:
            # Hash the password before saving
            agent.agent_password_hash = make_password(password)
        
        if commit:
            agent.save()
        
        return agent

class ForgotPasswordForm(forms.Form):
    agent_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'})
    )
    
    def clean_agent_email(self):
        email = self.cleaned_data.get('agent_email')
        if not Agent.objects.filter(agent_email=email).exists():
            raise forms.ValidationError("No account found with this email address")
        return email

class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit code'})
    )

class NewPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        
        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError("Passwords do not match")
        
        # Password strength validation
        if new_password:
            if len(new_password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long")
            if not re.search(r'[A-Z]', new_password):
                raise forms.ValidationError("Password must contain at least one uppercase letter")
            if not re.search(r'[a-z]', new_password):
                raise forms.ValidationError("Password must contain at least one lowercase letter")
            if not re.search(r'[0-9]', new_password):
                raise forms.ValidationError("Password must contain at least one number")
        
        return cleaned_data