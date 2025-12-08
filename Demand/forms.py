from django import forms
from .models import Demand

class DemandFormModel(forms.ModelForm):

    class Meta:
        model = Demand
        fields = ['name', 'description']
        
        widgets = {
            'name': forms.Select(attrs={'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'ex: Tecnologia da informação (TI)'}, choices=[('', 'Selecione a área de atuação'), ('TI', 'TI'), ('Marketing', 'Marketing'), ('RH', 'RH'), ('Financeiro', 'Financeiro'), ('Vendas', 'Vendas'), ('Atendimento ao Cliente', 'Atendimento ao Cliente'), ('Logística', 'Logística'), ('Produção', 'Produção'), ('Jurídico', 'Jurídico'), ('Pesquisa e Desenvolvimento', 'Pesquisa e Desenvolvimento'), ('Outros', 'Outros')]),  
            'description': forms.Textarea(attrs={'rows': 1, 'cols': 50,'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'ex: Infraestrutura de TI'}),  
           # 'value': forms.NumberInput(attrs={'class': 'inputs block w-80 pl-3 pr-1 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'placeholder': 'R$ 0,00'}),
        }
        labels  = {
            'name': 'Área de Atuação',
            'description': 'Descrição',
        }

