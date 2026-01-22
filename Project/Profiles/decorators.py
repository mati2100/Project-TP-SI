from django.shortcuts import redirect
from .models import AgentToken

def token_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.session.get('auth_token')
        agent_id = request.session.get('agent_id')

        if not token or not agent_id:
            return redirect('login')

        exists = AgentToken.objects.filter(
            token=token,
            agent_id=agent_id
        ).exists()

        if not exists:
            return redirect('login')

        return view_func(request, *args, **kwargs)

    return wrapper
