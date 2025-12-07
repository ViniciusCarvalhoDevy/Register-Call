from django import forms
from datetime import date
from Company.models import Company
from Demand.models import Demand
from .models import CallRegister
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

class CallRegisterForm(forms.ModelForm):
    class Meta:
        model = CallRegister
        fields = ['dateCall', 'company', 'collaborator', 'demand', 'observation', 'value']

        widgets = {
            'dateCall': forms.DateInput(attrs={
                'class': 'inputs cursor block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'type': 'date',
                'value': date.today(),
            }),
            'company': forms.Select(attrs={
                'class': 'inputs selects block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm',

            }),
            'collaborator': forms.TextInput(attrs={
                'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': 'ex: Vinicius Carvalho',
            }),
            'demand': forms.Select(attrs={
                'class': 'inputs selects block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            }),
            'observation': forms.Textarea(attrs={
                'rows': 3,
                'cols': 50,
                'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
                'placeholder': 'ex: Condição Especial...',
            }),
             'value': forms.NumberInput(attrs={'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'R$ 0,00'}),
        }
        labels = {
            'dateCall': 'Data do Contato',
            'company': 'Empresa',
            'collaborator': 'Colaborador',
            'demand': 'Demanda',
            'observation': 'Observação',
            'value': 'Valor',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Setting a default empty choice.
        self.fields['company'].empty_label = 'Selecione uma empresa'
        self.fields['demand'].empty_label = 'Selecione uma demanda'
        
        self.fields['company'].queryset = Company.objects.all().order_by('name')
        self.fields['demand'].queryset = Demand.objects.all().order_by('description')