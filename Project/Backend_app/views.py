from django.shortcuts import render
from .models import Agent
from .forms import LoginForm, AddAgentForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            agent_name = form.cleaned_data['agent_name']
            agent_pwd = form.cleaned_data['agent_pwd']
            
            try:
                agent = Agent.objects.get(agent_name=agent_name, agent_pwd=agent_pwd)

                if not agent.is_active:
                    form.add_error(None, "Ce compte est désactivé")
                else:

                    request.session['agent_id'] = agent.id
                    request.session['agent_name'] = agent.agent_name
                    return render(request, 'home.html', {'agent_name': agent.agent_name})
            except Agent.DoesNotExist:
                form.add_error(None, "Nom d'agent ou mot de passe incorrect")
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
                errors.append("Les mots de passe ne correspondent pas")
            
            if Agent.objects.filter(agent_name=agent_name).exists():
                errors.append("Ce nom d'agent existe déjà")
            
            if Agent.objects.filter(agent_email=agent_email).exists():
                errors.append("Cet email est déjà utilisé")
            
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
                    'success_message': 'Compte créé avec succès! Connectez-vous.'
                })
    else:
        form = AddAgentForm()
    
    return render(request, 'register.html', {'form': form})