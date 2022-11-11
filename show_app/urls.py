from django.urls import path
import show_app.views as views

urlpatterns = [
    path('<str:alias>/', views.link_show),
]
