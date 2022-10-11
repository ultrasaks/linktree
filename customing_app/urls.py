from django.urls import path
import customing_app.views as views

urlpatterns = [
    path('', views.home),
    path('links/', views.links),
    path('colors/', views.colors),

    path('colors/test/', views.link_test),

    path('create/', views.create_profile),
    path('colors/create/', views.create_scheme),
]
