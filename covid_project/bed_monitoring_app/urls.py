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

]
