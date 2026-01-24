# Profiles/decorators.py
from django.shortcuts import redirect
from django.utils import timezone
from .models import AgentToken

def token_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.session.get('auth_token')
        agent_id = request.session.get('agent_id')

        if not token or not agent_id:
            return redirect('login')

        try:
            agent_token = AgentToken.objects.get(
                token=token,
                agent_id=agent_id
            )
        except AgentToken.DoesNotExist:
            return redirect('login')

        # EXPIRATION CHECK
        if agent_token.is_expired():
            # cleanup
            agent_token.delete()
            request.session.flush()
            return redirect('login')

        return view_func(request, *args, **kwargs)

    return wrapper
