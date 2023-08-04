from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Post
from .serializers import UserSerializer, PostSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # После успешной регистрации перенаправляем на страницу списка пользователей
        else:
            # Отобразить ошибки формы
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('get_all_users')
        else:
            # Handle invalid credentials
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    first_user = users.first()
    can_create_post = request.user.is_authenticated and request.user == first_user

    return render(request, 'users_list.html', {'users': users, 'can_create_post': can_create_post})

@api_view(['GET'])
def get_user_posts(request, user_id):
    posts = Post.objects.filter(user_id=user_id)
    return render(request, 'user_posts_list.html', {'posts': posts})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        if post.user == request.user:
            post.delete()
            return Response(status=204)
        else:
            return Response({"error": "You can only delete your own posts."}, status=403)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=404)
