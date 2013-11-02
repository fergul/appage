from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(label="", required=True, max_length=30,
                                    widget=forms.TextInput(attrs={'class':'form-control',
                                                                  'autofocus':'',
                                                                  'placeholder':'First name'
                                                                  }))
    
    last_name = forms.CharField(label="", required=True, max_length=30,
                                widget=forms.TextInput(attrs={'class':'form-control',
                                                              'placeholder':'Last name'
                                                              }))
    
    email = forms.EmailField(label="", required=True,
                             widget=forms.TextInput(attrs={'class':'form-control',
                                                           'autofocus':'',
                                                           'placeholder':'Email address'
                                                           }))
    
    password = forms.CharField(label="", required=True, min_length=8,
                               widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                 'placeholder':'Password'
                                                                 }))
