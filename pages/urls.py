from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard.html'),
    path('log/<str:d>/', views.log, name='log.html'),
    path('lattest_data/', views.lattest_data),
    path('log_data/<str:d>/', views.log_data),
    path('peak_hours/', views.peak_hours),
    path('l-stat-api/', views.l_stat_api),
    path('l-stat/', views.l_stat),
    path('log-temp-hum-mot/<str:temp>/<str:hum>/<str:mot>/', views.log_temp_hum_mot),
    path('enviro-dashboard/', views.enviro_dashboard, name='enviro-dashboard.html'),
    path('enviro-lattest-data/', views.enviro_lattest_data),
    path('enviro-hist-chart/<str:d>/', views.enviro_his_data, name='enviro-hist-chart.html'),
]
