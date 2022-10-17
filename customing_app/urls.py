from django.urls import path
import customing_app.views as views

urlpatterns = [
    path('', views.home),
    path('links/', views.links),
    path('colors/', views.colors),

    path('colors/edit/', views.colors_edit),
    path('colors/test/', views.link_test),

    path('links/edit/', views.links_edit),
    path('links/new/', views.create_link),
    
    path('create/', views.create_profile),
    path('colors/create/', views.create_scheme),
    path('colors/change/', views.edit_scheme),
]
