from django.urls import path
from posts import views

urlpatterns = [
    path('users/', views.get_all_users, name='get_all_users'),
    path('users/<int:user_id>/posts/', views.get_user_posts, name='get_user_posts'),
    path('add_post/', views.add_post, name='add_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
]
