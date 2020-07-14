from django.shortcuts import render
from bed_monitoring_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from bed_monitoring_app.models import HospitalBedDetails, UserProfileInfo

# Create your views here.

def index(request):
    hospital_details_all = HospitalBedDetails.objects.all()
    user_hospital_names = UserProfileInfo.objects.all()
    users = User.objects.filter(is_superuser=False)
    details_list = []
    for user in users:
        for i in reversed(range(len(hospital_details_all))):
            if user == hospital_details_all[i].user:

                profile_details = UserProfileInfo.objects.filter(user=user)
                user_hospital_name = profile_details[0].hospital_name
                details_list.append(
                                    {'hospital_name':user_hospital_name,
                                    'total_no_of_beds':hospital_details_all[i].total_no_of_beds,
                                    'total_govt_beds':hospital_details_all[i].total_govt_beds,
                                    'total_hospital_beds':hospital_details_all[i].total_hospital_beds,
                                    'occupied_govt_beds':hospital_details_all[i].occupied_govt_beds,
                                    'occupied_hospital_beds':hospital_details_all[i].occupied_hospital_beds,
                                    })
                break
            else:
                continue
            # import pdb;pdb.set_trace()

    # hospital_details_all
    # import pdb;pdb.set_trace()
    return render(request,'bed_monitoring_app/index.html',{'beds_list': details_list})

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
                bed_details_user = HospitalBedDetails.objects.filter(user=user)
                if len(bed_details_user) == 0:
                    return HttpResponseRedirect(reverse('bed_monitoring_app:update_bed_details'))
                # bed_details_test= HospitalBedDetails.objects.filter(user=user)
                latest_object = len(bed_details_user)-1
                bed_details = bed_details_user[latest_object]
                beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                            'total_govt_beds': bed_details.total_govt_beds,
                            'total_hospital_beds': bed_details.total_hospital_beds,
                            'occupied_govt_beds': bed_details.occupied_govt_beds,
                            'occupied_hospital_beds': bed_details.occupied_hospital_beds, }
                # return HttpResponseRedirect(reverse('bed_monitoring_app:update_bed_details'))
                return render(request, 'bed_monitoring_app/first_page.html', {'beds_dict':beds_dict})
            else:
                return HttpResponse("Account not active")
        else:
            # print("Tried to login but failed")
            print("Username: {} and password {}".format(username, password))
            return render(request,'bed_monitoring_app/invalid_login.html')

    else:
        return render(request, 'bed_monitoring_app/login.html', {})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def about_us(request):
    return render(request, 'bed_monitoring_app/about_us.html')

def update_bed_details(request):
    if request.method == 'POST':
        print("in update details")

        h_bed_info = HospitalBedDetails()
        h_bed_info.user = request.user
        h_bed_info.total_no_of_beds = int(request.POST.get('no_of_beds'))
        h_bed_info.total_govt_beds = int(0.8 * (h_bed_info.total_no_of_beds))
        h_bed_info.total_hospital_beds = int(0.2 *(h_bed_info.total_no_of_beds))
        h_bed_info.save()
        beds_dict = {'total_no_of_beds':h_bed_info.total_no_of_beds,
                    'total_govt_beds': h_bed_info.total_govt_beds,
                    'total_hospital_beds': h_bed_info.total_hospital_beds,
                    'occupied_govt_beds': h_bed_info.occupied_govt_beds,
                    'occupied_hospital_beds': h_bed_info.occupied_hospital_beds, }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
    return render(request, 'bed_monitoring_app/update_bed_details.html')


def update_govt_beds(request):
    if request.method == 'POST':
        print("in update details")
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        gov_beds = int(request.POST.get('govt_beds'))
        if gov_beds > bed_details.total_govt_beds:
            return HttpResponse('Total no of govt beds updated exceeds the limit')
        bed_details.occupied_govt_beds = gov_beds
        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds, }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})


    return render(request, 'bed_monitoring_app/update_govt_beds.html')

def update_hos_beds(request):
    if request.method == 'POST':
        print("in update details")
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        # import pdb;pdb.set_trace()
        hos_beds = int(request.POST.get('hospital_beds'))
        if hos_beds > bed_details.total_hospital_beds:
            return HttpResponse('Total no of hospital beds updated exceeds the limit')
        bed_details.occupied_hospital_beds = hos_beds
        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds, }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})

    return render(request, 'bed_monitoring_app/update_hos_beds.html')

def page_after_login(request):
    return render(request,'bed_monitoring_app/first_page.html')
