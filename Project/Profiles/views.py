from django.shortcuts import render
from django.shortcuts import redirect
from .models import Agent, PasswordResetCode
from .forms import LoginForm, AddAgentForm, ForgotPasswordForm, VerifyCodeForm, NewPasswordForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            agent_name = form.cleaned_data['agent_name']
            agent_pwd = form.cleaned_data['agent_pwd']
            
            try:
                agent = Agent.objects.get(agent_name=agent_name, agent_pwd=agent_pwd)

                if not agent.is_active:
                    form.add_error(None, "This account is disabled")
                else:

                    request.session['agent_id'] = agent.id
                    request.session['agent_name'] = agent.agent_name
                    return redirect("dashboard:index")
            except Agent.DoesNotExist:
                form.add_error(None, "Agent name or password is incorrect")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def addagent_view(request):
    if request.method == 'POST':
        form = AddAgentForm(request.POST)
        if form.is_valid():
            agent_name = form.cleaned_data['agent_name']
            agent_email = form.cleaned_data['agent_email']
            agent_pwd = form.cleaned_data['agent_pwd']
            confirm_agent_pwd = form.cleaned_data['confirm_agent_pwd']
            
            errors = []

            if agent_pwd != confirm_agent_pwd:
                errors.append("Passwords do not match")
            
            if Agent.objects.filter(agent_name=agent_name).exists():
                errors.append("Agent name already taken")
            
            if Agent.objects.filter(agent_email=agent_email).exists():
                errors.append("Email already used")

            if errors:
                for error in errors:
                    form.add_error(None, error)
            else:

                Agent.objects.create(
                    agent_name=agent_name,
                    agent_email=agent_email,
                    agent_pwd=agent_pwd,
                    is_active=True
                )

                return render(request, 'login.html', {
                    'form': LoginForm(),
                    'success_message': 'Account created successfully. Please log in.'
                })
    else:
        form = AddAgentForm()
    
    return render(request, 'register.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            agent_email = form.cleaned_data['agent_email']
            
            try:
                # Chercher l'agent par email
                agent = Agent.objects.get(agent_email=agent_email)
                
                # Générer un nouveau code
                code = PasswordResetCode.generate_code()
                
                # Supprimer les anciens codes non utilisés
                PasswordResetCode.objects.filter(agent=agent, is_used=False).delete()
                
                # Créer le nouveau code
                reset_code = PasswordResetCode.objects.create(
                    agent=agent,
                    code=code
                )
                
                # Envoyer l'email (version basique)
                try:
                    # Configuration SMTP (à adapter selon ton fournisseur email)
                    # Pour Gmail par exemple
                    sender_email = "ton_email@gmail.com"  # À CHANGER
                    sender_password = "ton_mot_de_passe"  # À CHANGER
                    
                    message = MIMEMultipart("alternative")
                    message["Subject"] = "Réinitialisation de votre mot de passe"
                    message["From"] = sender_email
                    message["To"] = agent_email
                    
                    text = f"""Hello {agent.agent_name},
                    
You have requested a password reset.
Your verification code is: {code}

This code is valid for 15 minutes.

If you did not make this request, please ignore this email.
"""
                    
                    html = f"""<html>
<body>
    <h3>Hello {agent.agent_name},</h3>
    <p>You have requested a password reset.</p>
    <p>Your verification code is: <strong>{code}</strong></p>
    <p>This code is valid for 15 minutes.</p>
    <p>If you did not make this request, please ignore this email.</p>
</body>
</html>"""
                    
                    part1 = MIMEText(text, "plain")
                    part2 = MIMEText(html, "html")
                    
                    message.attach(part1)
                    message.attach(part2)
                    
                    # Connexion au serveur SMTP
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, agent_email, message.as_string())
                    
                    # Stocker l'ID de l'agent dans la session pour les étapes suivantes
                    request.session['reset_agent_id'] = agent.id
                    return render(request, 'verify_code.html', {
                        'form': VerifyCodeForm(),
                        'agent_email': agent_email,
                        'success_message': f'A verification code has been sent to {agent_email}'
                    })
                    
                except Exception as e:
                    # En cas d'erreur d'envoi d'email, on peut utiliser une méthode alternative
                    # Ici, on affiche juste le code dans la console pour le test
                    print(f"RESET CODE FOR {agent_email}: {code}")
                    
                    # Stocker l'ID de l'agent dans la session
                    request.session['reset_agent_id'] = agent.id
                    return render(request, 'verify_code.html', {
                        'form': VerifyCodeForm(),
                        'agent_email': agent_email,
                        'test_code': code,  # Pour le test, on affiche le code
                        'success_message': f'Test code (for developpement) for: {code}'
                    })
                    
            except Agent.DoesNotExist:
                form.add_error('agent_email', "No account found with this email")
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot_password.html', {'form': form})

def verify_code_view(request):
    # Vérifier si l'agent est en train de réinitialiser son mot de passe
    if 'reset_agent_id' not in request.session:
        return render(request, 'forgot_password.html', {
            'form': ForgotPasswordForm(),
            'error_message': 'Please first request a password reset'
        })
    
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            agent_id = request.session['reset_agent_id']
            
            try:
                # Chercher le code non utilisé et valide
                reset_code = PasswordResetCode.objects.get(
                    agent_id=agent_id,
                    code=code,
                    is_used=False
                )
                
                if reset_code.is_valid():
                    # Marquer le code comme utilisé
                    reset_code.is_used = True
                    reset_code.save()
                    
                    # Stocker dans la session pour l'étape suivante
                    request.session['verified_agent_id'] = agent_id
                    return render(request, 'new_password.html', {
                        'form': NewPasswordForm(),
                        'success_message': 'Code verified! Choose a new password'
                    })
                else:
                    form.add_error('code', 'This code has expired or has already been used')
                    
            except PasswordResetCode.DoesNotExist:
                form.add_error('code', 'Code invalide')
    else:
        form = VerifyCodeForm()
    
    return render(request, 'verify_code.html', {'form': form})

def new_password_view(request):
    # Vérifier si le code a été vérifié
    if 'verified_agent_id' not in request.session:
        return render(request, 'forgot_password.html', {
            'form': ForgotPasswordForm(),
            'error_message': 'Please first verify your code'
        })
    
    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']
            
            if new_password != confirm_new_password:
                form.add_error('confirm_new_password', "Passwords do not match")
            else:
                # Mettre à jour le mot de passe
                agent_id = request.session['verified_agent_id']
                try:
                    agent = Agent.objects.get(id=agent_id)
                    agent.agent_pwd = new_password
                    agent.save()
                    
                    # Nettoyer la session
                    if 'reset_agent_id' in request.session:
                        del request.session['reset_agent_id']
                    if 'verified_agent_id' in request.session:
                        del request.session['verified_agent_id']
                    
                    return render(request, 'login.html', {
                        'form': LoginForm(),
                        'success_message': 'Password changed successfully! Please log in with your new password'
                    })
                    
                except Agent.DoesNotExist:
                    form.add_error(None, "An error occurred")
    else:
        form = NewPasswordForm()
    
    return render(request, 'new_password.html', {'form': form})