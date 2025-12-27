from django.shortcuts import render,redirect
from django.views.generic import FormView
from CustomerUser.models import CustomerUser
from .forms import DemandFormModel
from django.http import HttpResponse
from django.contrib import messages
from .models import Demand
# Create your views here.
class DemandRegisterView(FormView):
    template_name = 'demandRegister.html'
    success_url = '/demand/register'
    form_class = DemandFormModel
    
    def form_valid(self, form):
        customerID = self.request.session.get('userAuthCustomerID')
        demands = Demand()
        demands.name = form.cleaned_data.get('name')
        demands.description = form.cleaned_data.get('description')
        user = CustomerUser.objects.get(id=customerID)
        demands.user = user

        try:
            demands.save()
            messages.add_message(self.request, messages.SUCCESS, 'Demanda cadastrada com sucesso!')
        except Exception as e:
            e.add_note("Erro em salvar dados para a inclusão da Demanad", str(e))
            messages.add_message(self.request, messages.ERROR, 'Erro ao cadastrar a Demanda!')
        return redirect('demandRegister')
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Erro ao cadastrar a Demanda! Verifique os dados informados.')
        return render(self.request, 'demandRegister.html', {'form': form})