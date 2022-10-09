from django.urls import path
import customing_app.views as views

urlpatterns = [
    path('', views.home),
    path('links/', views.links),
    path('colors/', views.colors),

    path('create/', views.create_profile),
]
