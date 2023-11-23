# simple_jquery_django_auto_logout
## 


Requirements:
- Django >=2.2,<4.0
- Jquery
- ✨ Coffee ✨

This is python package that make your web app autologout system look easier with minimal configurations
Adapted FROM [django-auto-logout](https://pypi.org/project/django-auto-logout/) package

## Installation

```sh
pip install simple_jquery_django_auto_logout
```


## Usage

Add This to your django settings.py
```sh
SIMPLE_AUTO_LOGOUT = {
    'AUTO_LOGOUT_IDLE_TIME' : timedelta(minutes=10),
    'AUTO_LOGOUT_MESSAGE' : 'Sesi Anda sudah habis, silahkan login kembali.',
    'AUTO_LOGOUT_URL' : 'app:logout',
}
```

Add this line to your context processor list
```sh
'simple_jquery_django_auto_logout.context_processors.auto_logout_context'
```

Add this to your base template or page that you want to activate auto logout
```sh
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
{{ jquery_django_auto_logout }}
```
And you are DONE !!! 
Test your web app, it should be auto logout after several time you depend on your settings value above.

## Note
If you want to add some message show while redirect to login page, you should use message framework from django
https://docs.djangoproject.com/en/3.2/ref/contrib/messages/ and add some configuration in your logout URL like 
```sh
@method_decorator(login_required(), name='dispatch')
class LogoutViews(View):
    def get(self, request):
        logout_message = request.GET.get('logout_message', None)
        if logout_message is not None:
            messages.info(request, logout_message)
        
        logout(request)
        return redirect(request.META['HTTP_REFERER'])
```
## License

MIT

**Free Software, Hell Yeah!**