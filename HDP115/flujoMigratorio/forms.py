from dataclasses import field
from pyexpat import model
from django import forms
from .models import Entrada, persona

class DateInput(forms.DateInput): 
    input_type = 'date'

#Formulario para Crear Personas
class PersonaForm(forms.ModelForm):
   
    class Meta:
        model = persona
        fields = ('nombre','apellido','tipoDocumento','pasaporte','dui','nacionalidad','estado')
        label = {
            
            'nombre':('Nombre de la persona'),
            'apellido':('Apellido de la persona'),
            
        }
        help_texts ={
           
            'nombre':('Campo obligatorio'),
            'apellido':('Campo obligatorio'),
            
        }

class EntradaForms(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ('fechaIngreso','TiempoPermanencia','paisOrigen')
        
        widgets = { 'fechaIngreso': DateInput(), }

class BuscarId(forms.Form):   
    buscar = forms.CharField(label='buscarID')
    