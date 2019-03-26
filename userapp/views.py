from django.shortcuts import render, HttpResponseRedirect
from userapp.forms import GiftUserLoginForm, GiftUserRegisterForm, GiftUserEditForm, GiftUserProfileEditForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from userapp.models import GiftUser
from django.db import transaction



def login(request):

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST':

        login_form = GiftUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('mainapp:main'))
    else:
        login_form = GiftUserLoginForm()

    content = {
        'login_form': login_form,
        'next': next
    }

    return render(request, 'userapp/login.html', content)

def login_after_registration(request):
    return render(request, 'userapp/login_a_r.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('mainapp:main'))


def register(request):

    if request.method == 'POST':
        register_form = GiftUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('userapp:login_a_r'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('userapp:login'))
    else:
        register_form = GiftUserRegisterForm()

    content = {
        'register_form': register_form,
    }

    return render(request, 'userapp/register.html', content)

# @login_required
# def edit(request):
#     basket = []
#     if request.user.is_authenticated:
#         basket = Basket.objects.filter(user=request.user)
#     if request.method == 'POST':
#         edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('auth:edit'))
#     else:
#         edit_form = ShopUserEditForm(instance=request.user)
#
#     content = {
#         'edit_form': edit_form,
#         'basket': basket,
#         'categories': categories
#     }
#
#     return render(request, 'edit.html', content)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.pk, user.activation_key])

    title = 'Подтверждение учетной записи {}'.format(user.username)

    message = 'Для подтверждения учетной записи {} на портале \
{} перейдите по ссылке: \n{}{}'.format(user.username, settings.DOMAIN_NAME, settings.DOMAIN_NAME, verify_link)

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, pk, activation_key):
    try:
        user = GiftUser.objects.get(pk=pk)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'userapp/verification.html')
        else:
            print('error activation user: {}'.format(user))
            return render(request, 'userapp/verification.html')
    except Exception as e:
        print('error activation user : {}'.format(e.args))
        return HttpResponseRedirect(reverse('authapp:login'))


@transaction.atomic
@login_required
def edit(request):

    if request.method == 'POST':
        edit_form = GiftUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = GiftUserProfileEditForm(request.POST, instance=request.user.giftuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = GiftUserEditForm(instance=request.user)
        profile_form = GiftUserProfileEditForm(
            instance=request.user.giftuserprofile
        )

    content = {
        'edit_form': edit_form,
        'profile_form': profile_form
    }
    return render(request, 'userapp/edit.html', content)