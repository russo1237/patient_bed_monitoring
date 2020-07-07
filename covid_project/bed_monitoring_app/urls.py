from django.urls import path
from bed_monitoring_app import views

#template URLs

app_name = 'bed_monitoring_app'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register, name = 'register'),
    path('user_login/', views.user_login, name = 'user_login'),
    path('about_us/', views.about_us, name = 'about_us'),
    path('update_details/', views.update_details, name ='update_details'),
    path('logout/', views.logout_view, name='logout'),
    path('first_page/', views.page_after_login, name = 'first_page'),

]
