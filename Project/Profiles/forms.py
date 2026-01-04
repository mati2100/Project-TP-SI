from django import forms
class LoginForm(forms.Form):
    agent_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Agent Name'})
    )
    agent_pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
class AddAgentForm(forms.Form):
    agent_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Agent Name'})
    )
    agent_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    agent_pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    confirm_agent_pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )


# Formulaire pour demander la réinitialisation
class ForgotPasswordForm(forms.Form):
    agent_email = forms.EmailField()

# Formulaire pour entrer le code
class VerifyCodeForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6)

# Formulaire pour le nouveau mot de passe
class NewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput)