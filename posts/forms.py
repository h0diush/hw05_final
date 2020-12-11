from django.forms import fields
from .models import Post,Comment
from django import forms



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        label = {'text': 'Введите текст', 'group': 'Выберите группу'}
        help_text = {
            'text': 'Напишите что-нибудь иньтересное',
            'group': 'Из уже существующих'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        label = {'text': 'Добавить комментарий'}
        help_text = {
            'text': 'Напишите Ваше мнение'}