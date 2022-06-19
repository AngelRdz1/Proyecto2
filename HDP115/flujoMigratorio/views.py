from multiprocessing import context
from re import I, template
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from .mixins import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class index(GroupRequiredMixin, TemplateView):
    group_required = [u'administrador',u'AgenteMigratorio']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        context=super().get_context_data(**kwargs)
        return super().dispatch(request, *args, **kwargs)
    template_name = 'index.html'

class registrarPersona(GroupRequiredMixin, CreateView):
    group_required = [u'administrador']
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    template_name = 'ingresarPersonas.html'
    model = persona
    form_class = PersonaForm

    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        return reverse_lazy('home')
    
    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
        personas = form.save(commit=False)
        
        try:
            personas.estado = 1
            form.save()
            messages.success(self.request, 'La Persona fue registrada con exito')
        except Exception:
            personas.delete()
            messages.success(self.request, 'Ocurrio un error al registrar la persona')
        return HttpResponseRedirect(self.get_url_redirect())

    
    
