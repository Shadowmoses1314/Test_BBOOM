from django.urls import path

from .views import (AboutPageView,
                    user_list,
                    user_posts,
                    delete_post,
                    create_post)

urlpatterns = [
    path('', user_list, name='user-list'),
    path('create_post/', create_post, name='create-post'),
    path('<int:user_id>/', user_posts, name='user-posts'),
    path('delete_post/<int:post_id>/', delete_post, name='delete-post'),
    path("about/", AboutPageView.as_view(), name="about"),
]
