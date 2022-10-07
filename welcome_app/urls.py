from django.urls import path
import welcome_app.views as views

urlpatterns = [
    path('', views.home),
    path('logout/', views.logout_view),
    path('login/', views.login_view),
    path('signup/', views.register_view)
]
