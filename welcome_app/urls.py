from django.urls import path
import welcome_app.views as views

urlpatterns = [
    path('', views.home),
]
