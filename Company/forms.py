from django import forms
from .models import Company

class CompanyFormModel(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'document', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'ex: Carvalhos Soluções'}),  
            'document': forms.TextInput(attrs={'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'ex: 00.000.000/0001-00'}),  
            'email': forms.EmailInput(attrs={'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'ex: empresa@gmail.com'}),
        }
        labels  = {
            'name': 'Razão Social',
            'document': 'CNPJ da Empresa',
            'email': 'Email da Empresa',
        }

    def clean_document(self):
        document = self.cleaned_data.get('document', '')
        # Remove qualquer caractere que não seja número
        document_numbers = ''.join(filter(str.isdigit, document))
        if len(document_numbers) != 14:
            raise forms.ValidationError('O CNPJ deve conter exatamente 14 dígitos numericos.')
        return document_numbers

