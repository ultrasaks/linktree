from django.urls import path
import customing_app.views as views

urlpatterns = [
    path('', views.home),
]