from django.urls import path
from bed_monitoring_app import views

#template URLs

app_name = 'bed_monitoring_app'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register, name = 'register'),
    path('user_login/', views.user_login, name = 'user_login'),
    path('about_us/', views.about_us, name = 'about_us'),
    path('update_bed_details/', views.update_bed_details, name ='update_bed_details'),
    path('update_govt_beds/', views.update_govt_beds, name ='update_govt_beds'),
    path('update_hos_beds/', views.update_hos_beds, name ='update_hos_beds'),
    path('logout/', views.logout_view, name='logout'),
    path('first_page/', views.page_after_login, name = 'first_page'),
    path('user_dashboard/', views.user_dashboard, name= 'user_dashboard'),
    path('update_all_bed_details/', views.update_all_bed_details, name ='update_all_bed_details'),
    path('update_o2_beds/', views.update_o2_beds, name ='update_o2_beds'),
    path('update_icu_details/', views.update_icu_details, name ='update_icu_details'),
    path('update_icu_ventilator_details/', views.update_icu_ventilator_details, name ='update_icu_ventilator_details'),
    path('update_beds_under_scheme_details/', views.update_beds_under_scheme_details, name ='update_beds_under_scheme_details'),
    path('update_total_icu_beds', views.update_total_icu_beds, name ='update_total_icu_beds'),
    path('update_total_o2_beds', views.update_total_o2_beds, name ='update_total_o2_beds'),
    path('update_total_icu_ventilator_beds', views.update_total_icu_ventilator_beds, name ='update_total_icu_ventilator_beds'),



]
