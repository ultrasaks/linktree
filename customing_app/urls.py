from django.urls import path
import customing_app.views as views
import customing_app.rest as rest

urlpatterns = [
    path('', views.home),
    path('links/', views.links),
    path('colors/', views.colors),

    path('colors/edit/', views.colors_edit),
    path('colors/test/', views.link_test),

    path('links/edit/legacy', views.links_edit),
    
    path('links/edit/', rest.edit_link_name),
    path('links/new/', rest.create_link),
    path('links/delete/', rest.delete_link),
    path('links/edit/pos/', rest.edit_pos),
    
    path('create/', rest.create_profile),
    path('colors/create/', rest.create_scheme),
    path('colors/change/', rest.edit_scheme),
]
