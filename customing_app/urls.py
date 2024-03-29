from django.urls import path
import customing_app.views as views
import customing_app.rest as rest

urlpatterns = [
    path('', views.home),
    path('links/', views.links),
    path('design/', views.colors),

    path('design/test/', views.link_test),
    path('design/fonts/', views.fonts_page),
    
    path('stats/', views.statistics),

    path('links/edit/', rest.edit_link_name),
    path('links/new/', rest.create_link),
    path('links/delete/', rest.delete_link),
    path('links/edit/pos/', rest.edit_pos),
    
    path('create/', rest.create_profile),
    path('design/create/', rest.create_scheme),
    path('design/change/color/', rest.change_color),
    path('design/change/font/', rest.change_font),
    path('design/change/font_type/', rest.change_font_type),
    path('design/change/button/', rest.change_button),
    path('design/change/shape/', rest.change_shape),

    path('new/font/', rest.get_new_font),
    

    path('change/', rest.edit_profile),
    path('image/', rest.upload_image),
    path('image/delete/', rest.delete_image),
]
