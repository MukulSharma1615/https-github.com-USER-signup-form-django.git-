from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import SignUpForm
from .token import account_activation_token
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.template import loader
from django.http import HttpResponse

@login_required
def home(request):
    return render(request, 'app/home.html')

def signup(request):
    print("welcome to signup view, Now you can see the magic ")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('app/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'app/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'app/account_activation_sent.html')