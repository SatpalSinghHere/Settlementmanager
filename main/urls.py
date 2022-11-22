from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('manage', views.manage, name='manage'),
    path('progressSettlement/<int:pk>', views.progress, name="progress_settlement")
    
]
