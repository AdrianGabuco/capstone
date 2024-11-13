
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session


class CustomSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the session for admin and employee separately based on cookies
        if request.user.is_authenticated:
            if hasattr(request.user, 'is_employee') and request.user.is_employee:
                session_key = f"employee_sessionid{request.user.id}"
            elif request.user.is_superuser:
                session_key = f"admin_sessionid{request.user.id}"
            else:
                session_key = None

            # If session is valid, use the corresponding session
            if session_key and session_key in request.COOKIES:
                request.session = self._get_session(session_key)
                
    def _get_session(self, session_key):
        # This method retrieves session data based on the custom session key
        try:
            session = Session.objects.get(session_key=session_key)
            return session
        except Session.DoesNotExist:
            return None