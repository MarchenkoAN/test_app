from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше ФИО', max_length=100)
    email = forms.EmailField(label='Ваш email', max_length=100)