from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('following/', views.following_list, name='following'),
    path('messages/', views.dialog_list, name='dialogs'),
    path('messages/<int:user_id>/', views.dialog, name='dialog'),
    path('messages/<int:user_id>/send/', views.send_message, name='send_message'),
]