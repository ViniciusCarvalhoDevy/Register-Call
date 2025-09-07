from django import forms
from datetime import date
from Company.models import Company
from Demand.models import Demand
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
    dateCall = forms.DateField(label='Data do Chamado', widget=forms.DateInput(attrs={'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm','type': 'date','value':date.today()}), required=True)
    company = forms.ChoiceField(label='Empresa', widget=forms.Select(attrs={'class': 'inputs selects block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}), required=True,choices=[('', 'Selecione uma empresa')] + [(company.id, company.name) for company in Company.objects.all().order_by('name')])
    colaborator = forms.CharField(label='Colaborador Solicitante', max_length=255, widget=forms.TextInput(attrs={'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'ex: Vinicius Carvalho'}), required=True)
    demand = forms.ChoiceField(label='Demanda Solicitada', widget=forms.Select(attrs={'class': 'inputs selects block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}), required=True, choices=[('', 'Selecione uma demanda')] + [(demand.id, demand.description) for demand in Demand.objects.all().order_by('description')])
    observation = forms.CharField(label='Observação', widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'ex: Condição Especial...'}), required=False)
