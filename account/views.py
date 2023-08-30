from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import RegistrationForm, UserEditForm
from .token import account_activation_token
from .models import UserBase
from orders.views import user_orders


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, 'store/account/user/dashboard.html', {'orders': orders,})

@login_required
def edit_details(request):

    changed_email = False
    activated_email = UserBase.objects.get(username=request.user).is_active

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            old_email = UserBase.objects.get(username=request.user).email
            new_email = user_form.cleaned_data['email']

            if old_email == new_email:
                user_form.save()
            else:
                user = user_form.save(commit=False)
                updated_fields = ['email', 'first_name', 'last_name', 'phone_number', 'country', 'city', 'postcode', 'address_line_1', 'address_line_2']

                for field in updated_fields:
                    setattr(user, field, user_form.cleaned_data[field])
                
                user.is_active = False
                user.save()

                # Setup email
                current_site = get_current_site(request)
                subject = 'Confirm Your Email Address'
                message = render_to_string('store/account/user/confirm_changed_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'old_email': old_email,
                    'flag': 'confirm-changed-email'
                })
                user.email_user(subject=subject, message=message)
                changed_email = True
                activated_email = False

    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'store/account/user/edit_details.html', {'user_form': user_form, 
                                                                    'changed_email': changed_email, 'activated_email': activated_email})

# Still have not figured out what to do with deleted users
# If a user is deleted and a new user tries to create an account with the same username and email as the deleted one,
# then username already exists and email is already taken errors will appear. This will happen because I do not really 
# delete the user I only set the is_active attribute to False
@login_required
def delete_user(request):
    user = UserBase.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return HttpResponse('You have succesfully deleted your account.') 

def account_register(request):

    if request.user.is_authenticated:
        return redirect('account:dashboard')
    
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('store/account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'flag': 'activate'
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'store/account/user/reset_status.html')
    else:
        registerForm = RegistrationForm()
    return render(request, 'store/account/registration/register.html', {'form': registerForm})

def account_activate(request, flag, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = UserBase.objects.get(pk=uid)
    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        if flag == 'activate':
            login(request, user)
            return redirect('account:dashboard')
        else:
            return redirect('account:edit_details')

    else:
        return HttpResponse('Invalid user')
    

