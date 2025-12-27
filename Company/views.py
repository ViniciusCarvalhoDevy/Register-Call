from django.shortcuts import render,redirect
from django.views.generic import FormView 
from .forms import CompanyFormModel
from CustomerUser.models import CustomerUser
from .models import Company
from django.contrib import messages
import re


# Create your views here.
class CompanyView(FormView):
    template_name = 'company/registerCompany.html'
    form_class = CompanyFormModel
    success_url = '/'

    def form_valid(self, form):
        customerID = self.request.session.get('userAuthCustomerID')
        company = Company()
        company.name = form.cleaned_data.get('name')
        company.document = form.cleaned_data.get('document')
        company.email = form.cleaned_data.get('email')
        print("Customer ID in CompanyView:", customerID)
        user = CustomerUser.objects.get(id=customerID)
        company.user = user
        try:
            company.save()
            messages.add_message(self.request, messages.SUCCESS, 'Empresa cadastrada com sucesso!')
        except Exception as e:
            e.add_note("Erro em salvar dados para a inclusão da Empresa")
            messages.add_message(self.request, messages.ERROR, 'Erro ao cadastrar a Empresa!')
        return redirect('registerCompany')
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, 'Verifique os dados informados.')
        return super().form_invalid(form)
    
    