from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Agent, AgentToken, PasswordResetCode
from .forms import LoginForm, AddAgentForm, ForgotPasswordForm, VerifyCodeForm, NewPasswordForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Profiles.decorators import token_required
from django.utils import timezone
from django.conf import settings
import random
import string

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
                    
                    # Create at refreche fi koul login 
                    token, created = AgentToken.objects.update_or_create(
                        agent=agent,
                         defaults={'created_at': timezone.now()}
                    )    
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

@token_required
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
            
            # Clear any existing verification session
            for key in ['reset_agent_id', 'reset_agent_email', 'verified_agent_id']:
                if key in request.session:
                    del request.session[key]
            
            try:
                agent = Agent.objects.get(agent_email=agent_email)
                
                # Delete old unused codes for this agent
                PasswordResetCode.objects.filter(agent=agent, is_used=False).delete()
                
                # Generate and save the verification code in database
                code = PasswordResetCode.generate_code()
                reset_code = PasswordResetCode.objects.create(agent=agent, code=code)
                
                # Send code via email
                subject = 'Password Reset Verification Code'
                message = f'Your verification code is: {code}\n\nThis code expires in 5 minutes.'
                sender_email = settings.EMAIL_HOST_USER
                recipient_email = agent_email
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))
                
                try:
                    # Use SMTP server to send email
                    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                        server.starttls()
                        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                        server.send_message(msg)
                except Exception as e:
                    print(f"Email error: {str(e)}")
                
                # Store agent_id in session for code verification
                request.session['reset_agent_id'] = agent.id
                request.session['reset_agent_email'] = agent_email
                
                return redirect('verify_code')
                
            except Agent.DoesNotExist:
                return render(request, 'forgot_password.html', {
                    'form': form,
                    'error_message': 'No agent found with this email address.'
                })
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot_password.html', {'form': form})

def verify_code_view(request):
    # Check if agent is in password reset process
    if 'reset_agent_id' not in request.session:
        return render(request, 'forgot_password.html', {
            'form': ForgotPasswordForm(),
            'error_message': 'Please first request a password reset.'
        })
    
    agent_email = request.session.get('reset_agent_email', '')
    
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip()  # Ensure code is clean
            agent_id = request.session['reset_agent_id']
            
            try:
                # Find the unused and valid code
                reset_code = PasswordResetCode.objects.filter(
                    agent_id=agent_id,
                    code=code,
                    is_used=False
                ).first()
                
                if reset_code is None:
                    # Code not found
                    return render(request, 'verify_code.html', {
                        'form': VerifyCodeForm(),
                        'agent_email': agent_email,
                        'error_message': 'Invalid code. Please check and try again.'
                    })
                
                if reset_code.is_valid():
                    # Mark code as used
                    reset_code.is_used = True
                    reset_code.save()
                    
                    # Store in session for next step
                    request.session['verified_agent_id'] = agent_id
                    request.session.modified = True  # Force save
                    
                    return redirect('new_password')
                else:
                    # Code has expired
                    return render(request, 'verify_code.html', {
                        'form': VerifyCodeForm(),
                        'agent_email': agent_email,
                        'error_message': 'This code has expired or has already been used. Please request a new code.'
                    })
                    
            except Exception as e:
                print(f"Error verifying code: {str(e)}")
                return render(request, 'verify_code.html', {
                    'form': VerifyCodeForm(),
                    'agent_email': agent_email,
                    'error_message': f'An error occurred. Please try again.'
                })
        else:
            # Form validation failed (not a 6-digit code)
            return render(request, 'verify_code.html', {
                'form': VerifyCodeForm(),
                'agent_email': agent_email,
                'error_message': 'Please enter a valid 6-digit code.'
            })
    else:
        form = VerifyCodeForm()
    
    return render(request, 'verify_code.html', {
        'form': form,
        'agent_email': agent_email
    })

def resend_code_view(request):
    # Check if agent is in password reset process
    if 'reset_agent_id' not in request.session:
        return redirect('forgot_password')
    
    agent_id = request.session['reset_agent_id']
    agent_email = request.session.get('reset_agent_email', '')
    
    # Clear verified_agent_id from session (start fresh)
    if 'verified_agent_id' in request.session:
        del request.session['verified_agent_id']
    
    request.session.modified = True  # Ensure session is saved
    
    try:
        agent = Agent.objects.get(id=agent_id)
        
        # Delete ALL old codes for this agent (both used and unused)
        PasswordResetCode.objects.filter(agent=agent).delete()
        
        # Generate and save new verification code
        code = PasswordResetCode.generate_code()
        reset_code = PasswordResetCode.objects.create(agent=agent, code=code)
        
        # Send code via email
        subject = 'Password Reset Verification Code (Resent)'
        message = f'Your new verification code is: {code}\n\nThis code expires in 5 minutes.'
        sender_email = settings.EMAIL_HOST_USER
        recipient_email = agent_email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        try:
            # Use SMTP server to send email
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            print(f"Email error: {str(e)}")
        
        # Redirect back to verify_code with success message
        return render(request, 'verify_code.html', {
            'form': VerifyCodeForm(),
            'agent_email': agent_email,
            'success_message': 'New code has been sent to your email! Please check your inbox.'
        })
        
    except Agent.DoesNotExist:
        return redirect('forgot_password')

def new_password_view(request):
    # Check if code has been verified
    if 'verified_agent_id' not in request.session:
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']
            
            # Form validation already checks this, but double-check
            if new_password != confirm_new_password:
                form.add_error('confirm_new_password', "Passwords do not match")
                return render(request, 'new_password.html', {'form': form})
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
                    
                    request.session.modified = True  # Force save
                    
                    messages.success(request, 'Password changed successfully! Please log in with your new password.')
                    return redirect('login')
                    
                except Agent.DoesNotExist:
                    form.add_error(None, "An error occurred. Agent not found.")
                    return render(request, 'new_password.html', {'form': form})
                except Exception as e:
                    form.add_error(None, f"An error occurred: {str(e)}")
                    return render(request, 'new_password.html', {'form': form})
        else:
            # Form validation failed
            return render(request, 'new_password.html', {'form': form})
    else:
        form = NewPasswordForm()
    
    return render(request, 'new_password.html', {'form': form})