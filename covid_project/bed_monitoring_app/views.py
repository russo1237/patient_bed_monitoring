from django.shortcuts import render
from bed_monitoring_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,'bed_monitoring_app/index.html')

def register(request):
    registered  = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            profile_form.save()

            registered = True
        else :
            print(user_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'bed_monitoring_app/registration.html',{'user_form': user_form,
                                        'profile_form':profile_form,
                                        'registered': registered})

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username= username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('bed_monitoring_app:update_details'))

            else:
                return HttpResponse("Account not active")
        else:
            print("Tried to login but failed")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login credentials")

    else:
        return render(request, 'bed_monitoring_app/login.html', {})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def about_us(request):
    return render(request, 'bed_monitoring_app/about_us.html')

def update_details(request):
    return render(request, 'bed_monitoring_app/update_details.html')
