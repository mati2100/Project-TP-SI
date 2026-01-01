from django import forms
class LoginForm(forms.Form):
    agent_name = forms.CharField(max_length=100)
    agent_pwd = forms.CharField(widget=forms.PasswordInput)

class AddAgentForm(forms.Form):
    agent_name = forms.CharField(max_length=100)
    agent_email = forms.EmailField()
    agent_pwd = forms.CharField(widget=forms.PasswordInput)
    confirm_agent_pwd = forms.CharField(widget=forms.PasswordInput)