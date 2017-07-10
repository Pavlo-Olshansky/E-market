from django.db.models import Q
from .models import UserProfile
from products.models import Game
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from .forms import SignUpForm, EditProfileForm, EditUserForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your E-market Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return render(request, 'registration/account_activation_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'registration/account_activation_invalid.html')


@login_required(login_url='/accounts/login/')
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
        user_sell_games = Game.objects.filter(author_id=pk)
    else:
        user = request.user
        user_sell_games = Game.objects.filter(author_id=request.user.id)
    
    user_buy_games = Game.objects.filter(~Q(author_id=request.user.id)).filter(is_accepted=True)

    context = {'user': user, 'user_sell_games': user_sell_games, 'user_buy_games': user_buy_games, 'pk': pk}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='/accounts/login/')
def edit_profile(request):

    if request.method == 'POST':
        
        # if request.POST.get("photoUpload"):
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        user_form = EditUserForm(request.POST, instance=request.user)

        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('accounts:view_profile'))

        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        profile_form = EditProfileForm(instance=request.user.userprofile)
        user_form = EditUserForm(instance=request.user)
    
    context = {'user_form': user_form, 'profile_form': profile_form,}
    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        context = {'form': form}
        return render(request, 'accounts/change_password.html', context)
