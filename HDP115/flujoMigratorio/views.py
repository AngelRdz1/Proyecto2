from multiprocessing import context
from re import I, template
from urllib import request
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from .mixins import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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
            form.save()
            messages.success(self.request, 'La Persona fue registrada con exito')
        except Exception:
            personas.delete()
            messages.success(self.request, 'Ocurrio un error al registrar la persona')
        return HttpResponseRedirect(self.get_url_redirect())

    
class entradaPersona(GroupRequiredMixin, CreateView):
    group_required = [u'administrador']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            personas = persona.objects.get(pk=self.kwargs['idp'])
        except Exception:
            messages.error(self.request, 'Ocurrió un error, la persona no existe')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    template_name = 'entradaPersona.html'
    model = Entrada
    form_class = EntradaForms
    second_form_class = PersonaForm

    def get_context_data(self, **kwargs): 
        context = super(entradaPersona, self).get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None)
        
        return context

    
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        return reverse_lazy('home')
        
    def get_form(self, form_class = None, **kwargs):
        form = super().get_form(form_class)
        idp = self.kwargs.get('idp', None)
        nacionalidad = persona.objects.get(idPersona = idp) 
        if nacionalidad.nacionalidad == 2:
            form.fields['TiempoPermanencia'].disabled = True
        return form

    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
        idp = self.kwargs.get('idp', None) 
        entrada = form.save(commit = False)
        personas = self.second_form_class(self.request.POST)
        try:
            per = persona.objects.get(idPersona = idp)
            per.estado = 2
            entrada.persona = per
            entrada.save()
            per.save()
            messages.success(self.request, 'Persona registrada con éxito')
        except Exception:
            entrada.delete()
            messages.error(self.request, 'Ocurrió un error al guardar la entrada de la persona al pais')
        return HttpResponseRedirect(self.get_url_redirect()) 
        
        
         


    

"""
class buscarEntrada(GroupRequiredMixin, CreateView):
    group_required = [u'administrador']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    template_name = 'buscarEntrada.html'
    form_class = EntradaForms
    def get_url_redirect(self, **kwargs):
        context=super().get_context_data(**kwargs)
        return reverse_lazy('home')
    
    def form_valid(self, form, **kwargs):
        context=super().get_context_data(**kwargs)
        persona = form.save(commit=False)
        
        try:
            
            messages.success(self.request, '')
        except Exception:
            persona.delete()
            messages.success(self.request, '')
        return HttpResponseRedirect(self.get_url_redirect())"""

class indexBuscarPersona(GroupRequiredMixin, ListView):
    group_required = [u'administrador']
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

   
    #busqueda = request.GET.get("buscar")
    form_class = BuscarId
    

    template_name = 'buscarEntrada.html'
    model = persona
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        per = persona.objects.all()
        busqueda = self.request.GET.get("buscar")
        if busqueda is not None:
            per= persona.objects.filter(
                Q(pasaporte = busqueda) |
                Q(dui = busqueda)
            ).distinct()        
        context['personas'] = per
        return context


"""contexto = {
        'persona': personas
    }
    return render(request, 'buscarEntrada.html', contexto)"""