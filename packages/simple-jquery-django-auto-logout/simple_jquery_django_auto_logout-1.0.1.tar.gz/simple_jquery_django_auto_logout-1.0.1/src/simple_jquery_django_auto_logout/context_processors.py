from .supports import seconds_until_idle_time_end, now
from django.urls import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

jquery_var = """ 
    <script type="text/javascript">
        var auto_logout_idle_time = parseFloat('%s');
        var timeoutInMiliseconds = Math.max(auto_logout_idle_time,0)*1000+999;
        var timeoutId; 
        
        function resetTimer() { 
            window.clearTimeout(timeoutId);
            startTimer();
        }

        function startTimer() { 
            timeoutId = window.setTimeout(doInactive, timeoutInMiliseconds);
        }
          
        function doInactive() {
            location.replace("%s");
        }
         
        function setupTimers () {
            document.addEventListener("mousemove", resetTimer, false);
            document.addEventListener("mousedown", resetTimer, false);
            document.addEventListener("keypress", resetTimer, false);
            document.addEventListener("touchmove", resetTimer, false);
             
            startTimer();
        }

        (function() {
            setupTimers();
        })();

    </script>
"""

def _trim(s: str) -> str:
    return ''.join([line.strip() for line in s.split('\n')])

def auto_logout_context(request):
    if request.user.is_anonymous:
        return {}

    options = getattr(settings, 'SIMPLE_AUTO_LOGOUT')
    if not options:
        return {}

    ctx = {}
    current_time = now()

    if 'AUTO_LOGOUT_IDLE_TIME' in options:
        ctx['AUTO_LOGOUT_MESSAGE'] = seconds_until_idle_time_end(request, options['AUTO_LOGOUT_IDLE_TIME'], current_time)

    if 'AUTO_LOGOUT_MESSAGE' in options:
        logout_message = options['AUTO_LOGOUT_MESSAGE']
    else:
        logout_message = 'Your session has been ended, please re-login again.'

    if 'AUTO_LOGOUT_URL' in options:

        ctx['AUTO_LOGOUT_URL'] = f"{reverse(options['AUTO_LOGOUT_URL'])}?logout_message={logout_message}"
    
    ctx['jquery_django_auto_logout'] = mark_safe(_trim(jquery_var % (ctx['AUTO_LOGOUT_MESSAGE'], ctx['AUTO_LOGOUT_URL'])))

    return ctx