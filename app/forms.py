from django import forms
from django.forms import  ModelForm, ClearableFileInput,TextInput,Textarea,SelectMultiple,EmailInput,PasswordInput
from django.forms import Select
from .models import *
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm


# class CreatePostForm(forms.ModelForm):
    

#     class Meta: 
#         model = post
#         fields = '__all__'
#         widgets = {
#             # 'cover': ClearableFileInput(attrs={'class': 'form-control-file'}),
#             'details': Textarea(attrs={'class':'form-control', 'cols':20,'rows':20}),
#         }
        
    


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name','username','email', 'password1', 'password2']
        widgets = { 
                   
                   'name': TextInput(attrs={'class':'form-control'}), 
                   'username': TextInput(attrs={'class':'form-control'}), 
                   'email': EmailInput(attrs={'class': 'form-control'}),
                   'password1': PasswordInput(attrs={'class':'form-control'}), 
                   'password2': PasswordInput(attrs={'class':'form-control'}), 
                   }





class CreatePostForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=True, help_text="Enter tags separated by commas")

    class Meta: 
        model = post
        fields = ['title', 'category', 'cover', 'tags', 'details']
        widgets = {
            'cover': ClearableFileInput(attrs={'class': 'form-control-file'}),
            'details': forms.Textarea(attrs={'class':'form-control', 'cols':20, 'rows':20}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),  # Add this line for tag field
        }    
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['tags'].help_text = "Enter tags separated by commas"
        
        
        
        
class PostForm(ModelForm):
    class Meta:
        model = post
        fields = ['title','category','cover','details']
        widgets = { 
                   
                   'title': TextInput(attrs={'class':'form-control'}), 
                   'category': Select(attrs={'class':'form-control','list':'category-list'}), 
                   'cover': ClearableFileInput(attrs={'class': 'form-control-file'}),
                   'details': TextInput(attrs={'class':'form-control'}), 
                   }
        
        
        


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['avatar','name','username', 'email', 'bio']
        exclude = ['password']
        
        widgets = { 
                   
                   'name': TextInput(attrs={'class':'form-control'}), 
                   'username': TextInput(attrs={'class':'form-control'}), 
                   'email': EmailInput(attrs={'class': 'form-control'}),
                   'bio': Textarea(attrs={'class':'form-control','cols':5, 'rows':8}), 
                   }
        
        


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
        for field_name in self.fields:
            if hasattr(self.fields[field_name].widget, 'attrs'):
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            self.fields[field_name].label = self.fields[field_name].label.capitalize()