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
                                    'total_hospital_beds': hospital_details_all[i].total_hospital_beds,
                                    'total_o2_beds': hospital_details_all[i].total_o2_beds,
                                    'total_icu_beds': hospital_details_all[i].total_icu_beds,
                                    'total_icu_ventilator_beds': hospital_details_all[i].total_icu_ventilator_beds,
                                    'total_beds_under_scheme' : hospital_details_all[i].total_beds_under_scheme,
                                    'occupied_govt_beds': hospital_details_all[i].occupied_govt_beds,
                                    'occupied_hospital_beds': hospital_details_all[i].occupied_hospital_beds,
                                    'occupied_o2_beds': hospital_details_all[i].occupied_o2_beds,
                                    'occupied_icu_beds': hospital_details_all[i].occupied_icu_beds,
                                    'occupied_icu_ventilator_beds': hospital_details_all[i].occupied_icu_ventilator_beds,
                                    'occupied_beds_under_scheme': hospital_details_all[i].occupied_beds_under_scheme,
                                    'remaining_govt_beds': hospital_details_all[i].total_govt_beds-hospital_details_all[i].occupied_govt_beds,
                                    'remaining_hos_beds': hospital_details_all[i].total_hospital_beds-hospital_details_all[i].occupied_hospital_beds,
                                    'remaining_o2_beds': hospital_details_all[i].total_o2_beds-hospital_details_all[i].occupied_o2_beds,
                                    'remaining_icu_beds': hospital_details_all[i].total_icu_beds-hospital_details_all[i].occupied_icu_beds,
                                    'remaining_icu_ventilator_beds': hospital_details_all[i].total_icu_ventilator_beds-hospital_details_all[i].occupied_icu_ventilator_beds,
                                    'remaining_beds_under_scheme': hospital_details_all[i].total_beds_under_scheme-hospital_details_all[i].occupied_beds_under_scheme,
                                    'phone_number':profile_details[0].phone_no,
                                    'address':profile_details[0].address
                                    })
                break
            else:
                continue
    return render(request,'bed_monitoring_app/index.html',{'beds_list': details_list})

def register(request):
    registered  = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        phone_no = request.POST.get('phone_no')
        length = len(phone_no)
        if (length < 9 or length>13):
            return render(request,'bed_monitoring_app/invalid_phone.html')
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
                    return HttpResponseRedirect(reverse('bed_monitoring_app:update_all_bed_details'))
                latest_object = len(bed_details_user)-1
                bed_details = bed_details_user[latest_object]
                beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                            'total_govt_beds': bed_details.total_govt_beds,
                            'total_hospital_beds': bed_details.total_hospital_beds,
                            'total_o2_beds': bed_details.total_o2_beds,
                            'total_icu_beds': bed_details.total_icu_beds,
                            'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                            'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                            'occupied_govt_beds': bed_details.occupied_govt_beds,
                            'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                            'occupied_o2_beds': bed_details.occupied_o2_beds,
                            'occupied_icu_beds': bed_details.occupied_icu_beds,
                            'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                            'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                            'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                            'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                            'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                            'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                            'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                            'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                             }
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

@login_required
def update_bed_details(request):
    if request.method == 'POST':
        print("in update details")
        object_h_bed = HospitalBedDetails.objects.filter(user=request.user)
        if len(object_h_bed)==0:
            h_bed_info = HospitalBedDetails()
            h_bed_info.user = request.user
            total_beds = int(request.POST.get('no_of_beds'))
            h_bed_info.total_no_of_beds = int(request.POST.get('no_of_beds'))
            h_bed_info.total_govt_beds = round(0.8 *  (h_bed_info.total_no_of_beds))
            h_bed_info.total_hospital_beds = round(0.2 * (h_bed_info.total_no_of_beds))
            # h_bed_info.total_beds_under_scheme = round(0.25 * (h_bed_info.total_govt_beds))
            h_bed_info.save()
            beds_dict = {'total_no_of_beds':h_bed_info.total_no_of_beds,
                        'total_govt_beds': h_bed_info.total_govt_beds,
                        'total_hospital_beds': h_bed_info.total_hospital_beds,
                        'occupied_govt_beds': h_bed_info.occupied_govt_beds,
                        'occupied_hospital_beds': h_bed_info.occupied_hospital_beds,
                        'remaining_govt_beds': h_bed_info.total_govt_beds-h_bed_info.occupied_govt_beds,
                        'remaining_hos_beds': h_bed_info.total_hospital_beds-h_bed_info.occupied_hospital_beds,

                         }
            return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})

        latest_object = object_h_bed[len(object_h_bed)-1]
        h_bed_info = HospitalBedDetails()
        h_bed_info.user = request.user
        h_bed_info.total_no_of_beds = int(request.POST.get('no_of_beds'))
        h_bed_info.total_govt_beds = round(0.8 *(h_bed_info.total_no_of_beds))
        h_bed_info.total_hospital_beds = round(0.2 *(h_bed_info.total_no_of_beds))
        h_bed_info.total_beds_under_scheme = round(0.25 * (h_bed_info.total_govt_beds))
        if (h_bed_info.total_no_of_beds < 0):
            return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
        h_bed_info.total_o2_beds = latest_object.total_o2_beds
        h_bed_info.total_icu_beds = latest_object.total_icu_beds
        h_bed_info.total_icu_ventilator_beds = latest_object.total_icu_ventilator_beds
        h_bed_info.occupied_govt_beds = latest_object.occupied_govt_beds
        h_bed_info.occupied_hospital_beds = latest_object.occupied_hospital_beds
        h_bed_info.occupied_o2_beds = latest_object.occupied_o2_beds
        h_bed_info.occupied_icu_beds = latest_object.occupied_icu_beds
        h_bed_info.occupied_icu_ventilator_beds = latest_object.occupied_icu_ventilator_beds
        h_bed_info.occupied_beds_under_scheme = latest_object.occupied_beds_under_scheme
        if h_bed_info.total_no_of_beds < latest_object.total_no_of_beds:
            if (h_bed_info.total_govt_beds < latest_object.occupied_govt_beds) or (h_bed_info.total_hospital_beds < latest_object.occupied_hospital_beds) :
                return HttpResponse("Total number of beds availbale at govt rate/hosptial rate are less than occupied beds at govt rate/hospital rate . Please check once")
        h_bed_info.save()
        beds_dict = {'total_no_of_beds':h_bed_info.total_no_of_beds,
                    'total_govt_beds': h_bed_info.total_govt_beds,
                    'total_hospital_beds': h_bed_info.total_hospital_beds,
                    'total_o2_beds': latest_object.total_o2_beds,
                    'total_icu_beds': latest_object.total_icu_beds,
                    'total_icu_ventilator_beds': latest_object.total_icu_ventilator_beds,
                    'total_beds_under_scheme' : h_bed_info.total_beds_under_scheme,
                    'occupied_govt_beds': latest_object.occupied_govt_beds,
                    'occupied_hospital_beds': latest_object.occupied_hospital_beds,
                    'occupied_o2_beds': latest_object.occupied_o2_beds,
                    'occupied_icu_beds': latest_object.occupied_icu_beds,
                    'occupied_icu_ventilator_beds': latest_object.occupied_icu_ventilator_beds,
                    'occupied_beds_under_scheme': latest_object.occupied_beds_under_scheme,
                    'remaining_govt_beds': h_bed_info.total_govt_beds-latest_object.occupied_govt_beds,
                    'remaining_hos_beds': h_bed_info.total_hospital_beds-latest_object.occupied_hospital_beds,
                    'remaining_o2_beds': latest_object.total_o2_beds-latest_object.occupied_o2_beds,
                    'remaining_icu_beds': latest_object.total_icu_beds-latest_object.occupied_icu_beds,
                    'remaining_icu_ventilator_beds': latest_object.total_icu_ventilator_beds-latest_object.occupied_icu_ventilator_beds,
                    'remaining_beds_under_scheme': h_bed_info.total_beds_under_scheme-latest_object.occupied_beds_under_scheme,
                     }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
    return render(request, 'bed_monitoring_app/update_bed_details.html')

@login_required
def update_govt_beds(request):
    if request.method == 'POST':
        print("in update details")
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        gov_beds = int(request.POST.get('govt_beds'))
        if (gov_beds < 0):
            return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
        if gov_beds > bed_details.total_govt_beds:
            return HttpResponse('Total no of govt beds updated exceeds the limit')
        bed_details.occupied_govt_beds = gov_beds

        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'total_o2_beds': bed_details.total_o2_beds,
                    'total_icu_beds': bed_details.total_icu_beds,
                    'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                    'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                    'occupied_o2_beds': bed_details.occupied_o2_beds,
                    'occupied_icu_beds': bed_details.occupied_icu_beds,
                    'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                    'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                    'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                    'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                    'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                    'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                    'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                    'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                     }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
    return render(request, 'bed_monitoring_app/update_govt_beds.html')

@login_required
def update_hos_beds(request):
    if request.method == 'POST':
        print("in update details")
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        hos_beds = int(request.POST.get('hospital_beds'))
        if (hos_beds < 0):
            return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
        if hos_beds > bed_details.total_hospital_beds:
            return HttpResponse('Total no of hospital beds updated exceeds the limit')
        bed_details.occupied_hospital_beds = hos_beds
        # if h_bed_info.total_no_of_beds < latest_object.total_no_of_beds:
        #     return HttpResponse("Total number of beds availbale at govt rate are less than occupied beds. Please check once")
        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'total_o2_beds': bed_details.total_o2_beds,
                    'total_icu_beds': bed_details.total_icu_beds,
                    'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                    'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                    'occupied_o2_beds': bed_details.occupied_o2_beds,
                    'occupied_icu_beds': bed_details.occupied_icu_beds,
                    'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                    'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                    'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                    'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                    'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                    'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                    'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                    'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                    }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})

    return render(request, 'bed_monitoring_app/update_hos_beds.html')

@login_required
def update_o2_beds(request):
    if request.method == 'POST':
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        o2_beds = int(request.POST.get('o2_Beds'))
        if (o2_beds < 0):
            return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
        if o2_beds > bed_details.total_o2_beds:
            return HttpResponse('Total no of O-2 beds updated exceeds the limit')
        bed_details.occupied_o2_beds = o2_beds
        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'total_o2_beds': bed_details.total_o2_beds,
                    'total_icu_beds': bed_details.total_icu_beds,
                    'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                    'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                    'occupied_o2_beds': bed_details.occupied_o2_beds,
                    'occupied_icu_beds': bed_details.occupied_icu_beds,
                    'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                    'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                    'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                    'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                    'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                    'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                    'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                    'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                     }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
    return render(request, 'bed_monitoring_app/update_o2_beds.html')

@login_required
def update_icu_details(request):
    if request.method == 'POST':
        print("in update details")
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        icu_beds = int(request.POST.get('icu_Beds'))
        if (icu_beds < 0):
            return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
        if icu_beds > bed_details.total_icu_beds:
            return HttpResponse('Total no of ICU beds updated exceeds the limit')
        bed_details.occupied_icu_beds = icu_beds
        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'total_o2_beds': bed_details.total_o2_beds,
                    'total_icu_beds': bed_details.total_icu_beds,
                    'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                    'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                    'occupied_o2_beds': bed_details.occupied_o2_beds,
                    'occupied_icu_beds': bed_details.occupied_icu_beds,
                    'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                    'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                    'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                    'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                    'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                    'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                    'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                    'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                     }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
    return render(request, 'bed_monitoring_app/update_icu_beds.html')


@login_required
def update_icu_ventilator_details(request):
    if request.method == 'POST':
        print("in update details")
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        icu_ventilator_beds = int(request.POST.get('ventilator_Beds'))
        if (icu_ventilator_beds < 0):
            return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
        if icu_ventilator_beds > bed_details.total_icu_ventilator_beds:
            return HttpResponse('Total no of ICU-ventilator beds updated exceeds the limit')
        bed_details.occupied_icu_ventilator_beds = icu_ventilator_beds
        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'total_o2_beds': bed_details.total_o2_beds,
                    'total_icu_beds': bed_details.total_icu_beds,
                    'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                    'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                    'occupied_o2_beds': bed_details.occupied_o2_beds,
                    'occupied_icu_beds': bed_details.occupied_icu_beds,
                    'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                    'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                    'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                    'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                    'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                    'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                    'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                    'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                     }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
    return render(request, 'bed_monitoring_app/update_icu_ventilator_beds.html')

@login_required
def update_total_icu_beds(request):
    if request.method == 'POST':
        print("in update details")
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        icu_beds = int(request.POST.get('no_of_icu_beds'))
        if (icu_beds< 0):
            return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
        if icu_beds < bed_details.total_icu_beds:
            if (icu_beds < bed_details.occupied_icu_beds):
                return HttpResponse('Total no of ICU beds are less than the occupied ICU beds currently')
        bed_details.total_icu_beds = icu_beds
        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'total_o2_beds': bed_details.total_o2_beds,
                    'total_icu_beds': bed_details.total_icu_beds,
                    'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                    'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                    'occupied_o2_beds': bed_details.occupied_o2_beds,
                    'occupied_icu_beds': bed_details.occupied_icu_beds,
                    'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                    'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                    'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                    'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                    'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                    'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                    'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                    'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                     }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
    return render(request, 'bed_monitoring_app/update_total_icu_beds.html')

@login_required
def update_total_o2_beds(request):
    if request.method == 'POST':
        print("in update details")
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        o2_beds = int(request.POST.get('no_of_o2_beds'))
        if (o2_beds < 0):
            return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
        if o2_beds < bed_details.total_o2_beds:
            if o2_beds < bed_details.occupied_o2_beds:
                return HttpResponse('Total no of O-2 beds are less than the occupied O-2 beds currently')
        bed_details.total_o2_beds = o2_beds
        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'total_o2_beds': bed_details.total_o2_beds,
                    'total_icu_beds': bed_details.total_icu_beds,
                    'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                    'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                    'occupied_o2_beds': bed_details.occupied_o2_beds,
                    'occupied_icu_beds': bed_details.occupied_icu_beds,
                    'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                    'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                    'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                    'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                    'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                    'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                    'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                    'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                     }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
    return render(request, 'bed_monitoring_app/update_total_o2_beds.html')

@login_required
def update_total_icu_ventilator_beds(request):
    if request.method == 'POST':
        print("in update details")
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        icu_vent_beds = int(request.POST.get('no_of_iv_beds'))
        if (icu_vent_beds < 0):
            return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
        if icu_vent_beds < bed_details.total_icu_ventilator_beds:
            if icu_vent_beds < bed_details.occupied_icu_ventilator_beds:
                return HttpResponse('Total no of ICU-ventilator beds are less than the occupied ICU-ventilator beds currently')
        bed_details.total_icu_ventilator_beds = icu_vent_beds
        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'total_o2_beds': bed_details.total_o2_beds,
                    'total_icu_beds': bed_details.total_icu_beds,
                    'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                    'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                    'occupied_o2_beds': bed_details.occupied_o2_beds,
                    'occupied_icu_beds': bed_details.occupied_icu_beds,
                    'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                    'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                    'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                    'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                    'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                    'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                    'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                    'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                     }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
    return render(request, 'bed_monitoring_app/update_total_icu_ventilator_beds.html')

@login_required
def update_beds_under_scheme_details(request):
    if request.method == 'POST':
        print("in update details")
        user = request.user
        bed_details_user = HospitalBedDetails.objects.filter(user=user)
        latest_object = len(bed_details_user)-1
        bed_details = bed_details_user[latest_object]
        scheme_beds = int(request.POST.get('scheme_Beds'))
        if (scheme_beds < 0):
            return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
        if scheme_beds > bed_details.total_beds_under_scheme:
            return HttpResponse('Total no of beds under scheme updated exceeds the limit')
        bed_details.occupied_beds_under_scheme = scheme_beds
        bed_details.save()
        beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                    'total_govt_beds': bed_details.total_govt_beds,
                    'total_hospital_beds': bed_details.total_hospital_beds,
                    'total_o2_beds': bed_details.total_o2_beds,
                    'total_icu_beds': bed_details.total_icu_beds,
                    'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                    'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                    'occupied_govt_beds': bed_details.occupied_govt_beds,
                    'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                    'occupied_o2_beds': bed_details.occupied_o2_beds,
                    'occupied_icu_beds': bed_details.occupied_icu_beds,
                    'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                    'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                    'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                    'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                    'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                    'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                    'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                    'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                     }
        return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
    return render(request, 'bed_monitoring_app/update_beds_under_scheme.html')





@login_required
def update_all_bed_details(request):
    if request.method=="POST":
        print("In update all bed details")
        object_h_bed = HospitalBedDetails.objects.filter(user=request.user)
        if len(object_h_bed)==0:
            h_bed_info = HospitalBedDetails()
            h_bed_info.user = request.user
            total_beds = int(request.POST.get('no_of_beds'))
            h_bed_info.total_no_of_beds = int(request.POST.get('no_of_beds'))
            if (h_bed_info.total_no_of_beds < 0):
                return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
            h_bed_info.total_govt_beds = round(0.8 *  (h_bed_info.total_no_of_beds))
            h_bed_info.total_hospital_beds = round(0.2 * (h_bed_info.total_no_of_beds))
            h_bed_info.total_o2_beds = int(request.POST.get('no_of_o2_beds'))
            if (h_bed_info.total_o2_beds < 0):
                return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
            h_bed_info.total_icu_beds = int(request.POST.get('no_of_icu_beds'))
            if (h_bed_info.total_icu_beds < 0):
                return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
            h_bed_info.total_icu_ventilator_beds = int(request.POST.get('no_of_icu_ventilator_beds'))
            if (h_bed_info.total_icu_ventilator_beds < 0):
                return HttpResponse("You have entered negative value. Beds can not be negative.Enter valid number for beds.")
            h_bed_info.total_beds_under_scheme = round(0.25 * (h_bed_info.total_govt_beds))
            h_bed_info.save()
            beds_dict = {'total_no_of_beds':h_bed_info.total_no_of_beds,
                        'total_govt_beds': h_bed_info.total_govt_beds,
                        'total_hospital_beds': h_bed_info.total_hospital_beds,
                        'total_o2_beds': h_bed_info.total_o2_beds,
                        'total_icu_beds': h_bed_info.total_icu_beds,
                        'total_icu_ventilator_beds': h_bed_info.total_icu_ventilator_beds,
                        'total_beds_under_scheme' : h_bed_info.total_beds_under_scheme,
                        'occupied_govt_beds': h_bed_info.occupied_govt_beds,
                        'occupied_hospital_beds': h_bed_info.occupied_hospital_beds,
                        'occupied_o2_beds': h_bed_info.occupied_o2_beds,
                        'occupied_icu_beds': h_bed_info.occupied_icu_beds,
                        'occupied_icu_ventilator_beds': h_bed_info.occupied_icu_ventilator_beds,
                        'occupied_beds_under_scheme': h_bed_info.occupied_beds_under_scheme,
                        'remaining_govt_beds': h_bed_info.total_govt_beds-h_bed_info.occupied_govt_beds,
                        'remaining_hos_beds': h_bed_info.total_hospital_beds-h_bed_info.occupied_hospital_beds,
                        'remaining_o2_beds': h_bed_info.total_o2_beds-h_bed_info.occupied_o2_beds,
                        'remaining_icu_beds': h_bed_info.total_icu_beds-h_bed_info.occupied_icu_beds,
                        'remaining_icu_ventilator_beds': h_bed_info.total_icu_ventilator_beds-h_bed_info.occupied_icu_ventilator_beds,
                        'remaining_beds_under_scheme': h_bed_info.total_beds_under_scheme-h_bed_info.occupied_beds_under_scheme,
                         }
            return render(request, 'bed_monitoring_app/hospital_info.html', {'beds_dict':beds_dict})
        latest_object = object_h_bed[len(object_h_bed)-1]
        h_bed_info = HospitalBedDetails()
        print("Code breaked in update all bed details")

    return render(request,'bed_monitoring_app/update_all_bed_details.html')

@login_required
def page_after_login(request):
    return render(request,'bed_monitoring_app/first_page.html')

# @login_required
def user_dashboard(request):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            bed_details_user = HospitalBedDetails.objects.filter(user=request.user)
            length_bed_details = len(bed_details_user)
            if length_bed_details==0:
                return render(request,'bed_monitoring_app/login.html')
            latest_object = len(bed_details_user)-1
            bed_details = bed_details_user[latest_object]
            beds_dict = {'total_no_of_beds':bed_details.total_no_of_beds,
                        'total_govt_beds': bed_details.total_govt_beds,
                        'total_hospital_beds': bed_details.total_hospital_beds,
                        'total_o2_beds': bed_details.total_o2_beds,
                        'total_icu_beds': bed_details.total_icu_beds,
                        'total_icu_ventilator_beds': bed_details.total_icu_ventilator_beds,
                        'total_beds_under_scheme' : bed_details.total_beds_under_scheme,
                        'occupied_govt_beds': bed_details.occupied_govt_beds,
                        'occupied_hospital_beds': bed_details.occupied_hospital_beds,
                        'occupied_o2_beds': bed_details.occupied_o2_beds,
                        'occupied_icu_beds': bed_details.occupied_icu_beds,
                        'occupied_icu_ventilator_beds': bed_details.occupied_icu_ventilator_beds,
                        'occupied_beds_under_scheme': bed_details.occupied_beds_under_scheme,
                        'remaining_govt_beds': bed_details.total_govt_beds-bed_details.occupied_govt_beds,
                        'remaining_hos_beds': bed_details.total_hospital_beds-bed_details.occupied_hospital_beds,
                        'remaining_o2_beds': bed_details.total_o2_beds-bed_details.occupied_o2_beds,
                        'remaining_icu_beds': bed_details.total_icu_beds-bed_details.occupied_icu_beds,
                        'remaining_icu_ventilator_beds': bed_details.total_icu_ventilator_beds-bed_details.occupied_icu_ventilator_beds,
                        'remaining_beds_under_scheme': bed_details.total_beds_under_scheme-bed_details.occupied_beds_under_scheme,
                         }
            return render(request, 'bed_monitoring_app/first_page.html', {'beds_dict':beds_dict})
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
                                        'total_hospital_beds': hospital_details_all[i].total_hospital_beds,
                                        'total_o2_beds': hospital_details_all[i].total_o2_beds,
                                        'total_icu_beds': hospital_details_all[i].total_icu_beds,
                                        'total_icu_ventilator_beds': hospital_details_all[i].total_icu_ventilator_beds,
                                        'total_beds_under_scheme' : hospital_details_all[i].total_beds_under_scheme,
                                        'occupied_govt_beds': hospital_details_all[i].occupied_govt_beds,
                                        'occupied_hospital_beds': hospital_details_all[i].occupied_hospital_beds,
                                        'occupied_o2_beds': hospital_details_all[i].occupied_o2_beds,
                                        'occupied_icu_beds': hospital_details_all[i].occupied_icu_beds,
                                        'occupied_icu_ventilator_beds': hospital_details_all[i].occupied_icu_ventilator_beds,
                                        'occupied_beds_under_scheme': hospital_details_all[i].occupied_beds_under_scheme,
                                        'remaining_govt_beds': hospital_details_all[i].total_govt_beds-hospital_details_all[i].occupied_govt_beds,
                                        'remaining_hos_beds': hospital_details_all[i].total_hospital_beds-hospital_details_all[i].occupied_hospital_beds,
                                        'remaining_o2_beds': hospital_details_all[i].total_o2_beds-hospital_details_all[i].occupied_o2_beds,
                                        'remaining_icu_beds': hospital_details_all[i].total_icu_beds-hospital_details_all[i].occupied_icu_beds,
                                        'remaining_icu_ventilator_beds': hospital_details_all[i].total_icu_ventilator_beds-hospital_details_all[i].occupied_icu_ventilator_beds,
                                        'remaining_beds_under_scheme': hospital_details_all[i].total_beds_under_scheme-hospital_details_all[i].occupied_beds_under_scheme
                                        })
                    break
                else:
                    continue
        return render(request,'bed_monitoring_app/index.html',{'beds_list': details_list})
    return render(request, 'bed_monitoring_app.about_us.html')
