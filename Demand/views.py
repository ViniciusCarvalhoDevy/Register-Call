from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import DemandFormModel
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
class DemandRegisterView(FormView):
    template_name = 'demandRegister.html'
    success_url = '/demand/register'
    form_class = DemandFormModel
    
    def form_valid(self, form):
        try:
            forms = DemandFormModel(self.request.POST)
            forms.save(commit=True)
            messages.add_message(self.request, messages.SUCCESS, 'Demanda cadastrada com sucesso!')
        except Exception as e:
            e.add_note("Erro em salvar dados para a inclusão da Demanad")
            messages.add_message(self.request, messages.ERROR, 'Erro ao cadastrar a Demanda!')
        return redirect('demandRegister')
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Erro ao cadastrar a Demanda! Verifique os dados informados.')
        return render(self.request, 'demandRegister.html', {'form': form})