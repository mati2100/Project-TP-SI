from django.shortcuts import render
from .models import Agent
from .forms import LoginForm, AddAgentForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            agent_name = form.cleaned_data['agent_name']
            agent_pwd = form.cleaned_data['agent_pwd']
            
            # Vérifier manuellement les identifiants
            try:
                agent = Agent.objects.get(agent_name=agent_name, agent_pwd=agent_pwd)
                # Vérifier si le compte est actif
                if not agent.is_active:
                    form.add_error(None, "Ce compte est désactivé")
                else:
                    # Créer une session simple
                    request.session['agent_id'] = agent.id
                    request.session['agent_name'] = agent.agent_name
                    request.session['agent_role'] = agent.role
                    return render(request, 'home.html', {'agent_name': agent.agent_name, 'agent_role': agent.role})
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
            role = form.cleaned_data['role']
            agent_pwd = form.cleaned_data['agent_pwd']
            confirm_agent_pwd = form.cleaned_data['confirm_agent_pwd']
            
            # Validation manuelle dans views.py
            errors = []
            
            # 1. Vérifier la correspondance des mots de passe
            if agent_pwd != confirm_agent_pwd:
                errors.append("Les mots de passe ne correspondent pas")
            
            # 2. Vérifier si l'agent existe déjà
            if Agent.objects.filter(agent_name=agent_name).exists():
                errors.append("Ce nom d'agent existe déjà")
            
            # 3. Vérifier si l'email existe déjà
            if Agent.objects.filter(agent_email=agent_email).exists():
                errors.append("Cet email est déjà utilisé")
            
            # S'il y a des erreurs, les ajouter au formulaire
            if errors:
                for error in errors:
                    form.add_error(None, error)
            else:
                # Créer le nouvel agent
                Agent.objects.create(
                    agent_name=agent_name,
                    agent_email=agent_email,
                    agent_pwd=agent_pwd,
                    role=role,
                    is_active=True
                )
                # Rediriger vers la page de connexion
                return render(request, 'login.html', {
                    'form': LoginForm(),
                    'success_message': 'Compte créé avec succès! Connectez-vous.'
                })
    else:
        form = AddAgentForm()
    
    return render(request, 'register.html', {'form': form})