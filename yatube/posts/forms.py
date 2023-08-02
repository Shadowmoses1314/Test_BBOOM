from django import forms

from .models import Group, Post, Comment


class PostForm(forms.ModelForm):
    text = forms.CharField()
    group = forms.ModelChoiceField(
        label='Группа', required=False,
        queryset=Group.objects.all(), help_text='тут хэлп текст')

    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        labels = {
            'text': ('Текст нового поста'),
            'group': ('Группа'),
            'image': ('Картинка')
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
