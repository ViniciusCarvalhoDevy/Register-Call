from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, required=True,widget=forms.EmailInput(attrs={'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'seuemail@exemplo.com'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': '••••••••'}), required=True,)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Password is required.")
        return password
    
class CallRegisterForm(forms.Form):
    pass
