from django import forms
from .models import Demand

class DemandFormModel(forms.ModelForm):

    class Meta:
        model = Demand
        fields = ['name', 'description', 'value']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'ex: Tecnologia da informação (TI)'}),  
            'description': forms.Textarea(attrs={'rows': 1, 'cols': 50,'class': 'block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'ex: Infraestrutura de TI'}),  
            'value': forms.NumberInput(attrs={'class': 'block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'R$ 0,00'}),
        }
        labels  = {
            'name': 'Nome',
            'description': 'Descrição',
            'value': 'Valor Por cada Demanda',
        }