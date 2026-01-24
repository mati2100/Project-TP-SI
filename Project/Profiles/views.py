from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Agent, AgentToken, PasswordResetCode
from .forms import LoginForm, AddAgentForm, ForgotPasswordForm, VerifyCodeForm, NewPasswordForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            agent_username = form.cleaned_data['agent_username']
            agent_password = form.cleaned_data['agent_password']
            
            try:
                agent = Agent.objects.get(agent_username=agent_username)
                
                # Verify password using check_password
                if not check_password(agent_password, agent.agent_password_hash):
                    form.add_error(None, "Invalid username or password")
                elif agent.agent_account_status != 'active':
                    form.add_error(None, "Your account is not active. Please contact administrator.")
                else:
                    # Store session data
                    request.session['agent_id'] = agent.id
                    request.session['agent_name'] = f"{agent.agent_first_name} {agent.agent_last_name}"
                    
                    # Create or get token
                    token, created = AgentToken.objects.get_or_create(agent=agent)
                    request.session['auth_token'] = str(token.token)
                    
                    # redirect to dashboard
                    return redirect('dashboard:index')
                    
            except Agent.DoesNotExist:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    agent_id = request.session.get('agent_id')
    
    if agent_id:
        AgentToken.objects.filter(agent_id=agent_id).delete()
    
    request.session.flush()
    return redirect('login')

def home_view(request):
    if 'agent_id' not in request.session:
        return redirect('login')
    
    agent_id = request.session['agent_id']
    try:
        agent = Agent.objects.get(id=agent_id)
        return render(request, 'home.html', {
            'agent_name': f"{agent.agent_first_name} {agent.agent_last_name}"
        })
    except Agent.DoesNotExist:
        request.session.flush()
        return redirect('login')

def addagent_view(request):
    if request.method == 'POST':
        form = AddAgentForm(request.POST)
        if form.is_valid():
            try:
                # Save the agent (form.save() handles password hashing)
                agent = form.save()
                
                return redirect('login')
            except Exception as e:
                form.add_error(None, f"Error creating account: {str(e)}")
    else:
        form = AddAgentForm()
    
    return render(request, 'register.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            agent_email = form.cleaned_data['agent_email']
            
            try:
                agent = Agent.objects.get(agent_email=agent_email)
                
                # Generate a new code
                code = PasswordResetCode.generate_code()
                
                # Delete old unused codes
                PasswordResetCode.objects.filter(agent=agent, is_used=False).delete()
                
                # Create the new code
                reset_code = PasswordResetCode.objects.create(
                    agent=agent,
                    code=code
                )
                
                # Store agent ID in session for next steps
                request.session['reset_agent_id'] = agent.id
                request.session['reset_agent_email'] = agent_email
                
                # Try to send email (simplified for now)
                try:
                    # For development, just print the code
                    print(f"PASSWORD RESET CODE FOR {agent_email}: {code}")
                    
                    # You can implement email sending here if needed
                    # For now, we'll just show it on the verify page for testing
                    
                    return render(request, 'verify_code.html', {
                        'form': VerifyCodeForm(),
                        'agent_email': agent_email,
                        'test_code': code,  # For development/testing only
                        'success_message': f'A verification code has been generated. Test code: {code}'
                    })
                    
                except Exception as e:
                    print(f"Error sending email: {e}")
                    # Fall back to showing code
                    return render(request, 'verify_code.html', {
                        'form': VerifyCodeForm(),
                        'agent_email': agent_email,
                        'test_code': code,
                        'success_message': f'Test code (for development): {code}'
                    })
                    
            except Agent.DoesNotExist:
                # Form validation already handles this, but just in case
                form.add_error('agent_email', "No account found with this email")
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot_password.html', {'form': form})

def verify_code_view(request):
    # Check if agent is in password reset process
    if 'reset_agent_id' not in request.session:
        return render(request, 'forgot_password.html', {
            'form': ForgotPasswordForm(),
            'error_message': 'Please first request a password reset'
        })
    
    agent_email = request.session.get('reset_agent_email', '')
    
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            agent_id = request.session['reset_agent_id']
            
            try:
                # Find the unused and valid code
                reset_code = PasswordResetCode.objects.get(
                    agent_id=agent_id,
                    code=code,
                    is_used=False
                )
                
                if reset_code.is_valid():
                    # Mark code as used
                    reset_code.is_used = True
                    reset_code.save()
                    
                    # Store in session for next step
                    request.session['verified_agent_id'] = agent_id
                    return render(request, 'new_password.html', {
                        'form': NewPasswordForm(),
                        'success_message': 'Code verified! Choose a new password'
                    })
                else:
                    form.add_error('code', 'This code has expired or has already been used')
                    
            except PasswordResetCode.DoesNotExist:
                form.add_error('code', 'Invalid code')
    else:
        form = VerifyCodeForm()
    
    return render(request, 'verify_code.html', {
        'form': form,
        'agent_email': agent_email
    })

def new_password_view(request):
    # Check if code has been verified
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
            
            # Form validation already checks this, but double-check
            if new_password != confirm_new_password:
                form.add_error('confirm_new_password', "Passwords do not match")
            else:
                # Update the password
                agent_id = request.session['verified_agent_id']
                try:
                    agent = Agent.objects.get(id=agent_id)
                    # Hash and save the new password
                    agent.agent_password_hash = make_password(new_password)
                    agent.save()
                    
                    # Clean up session
                    for key in ['reset_agent_id', 'reset_agent_email', 'verified_agent_id']:
                        if key in request.session:
                            del request.session[key]
                    
                    return render(request, 'login.html', {
                        'form': LoginForm(),
                        'success_message': 'Password changed successfully! Please log in with your new password'
                    })
                    
                except Agent.DoesNotExist:
                    form.add_error(None, "An error occurred")
    else:
        form = NewPasswordForm()
    
    return render(request, 'new_password.html', {'form': form})