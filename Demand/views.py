from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import DemandFormModel
from django.http import HttpResponse

# Create your views here.
class DemandRegisterView(FormView):
    template_name = 'demandRegister.html'
    success_url = '/demand/register'
    form_class = DemandFormModel
    
    def form_valid(self, form):
        try:
            forms = DemandFormModel(self.request.POST)
            forms.save(commit=False)
            print(forms.cleaned_data.POST)
        except Exception as e:
            e.add_note("Erro em salvar dados para a inclusão da Demanad")
        return HttpResponse('Demanda cadastrada com sucesso!')
    
    def form_invalid(self, form):
        pass
        return render(self.request, 'demandRegister.html', {'form': form})