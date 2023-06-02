from django.urls import path
import welcome_app.views as views
import welcome_app.rest as rest

urlpatterns = [
    path('', views.home),
    path('logout/', views.logout_view),
    path('login/', views.login_view),
    path('signup/', views.register_view),

    path('signup/first/', rest.register_part_1)
]
