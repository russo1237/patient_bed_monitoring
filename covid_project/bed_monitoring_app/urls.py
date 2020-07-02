from django.urls import path
from bed_monitoring_app import views

#template URLs

app_name = 'bed_monitoring_app'

urlpatterns = [
    path('', views.index, name = 'index'),
]
