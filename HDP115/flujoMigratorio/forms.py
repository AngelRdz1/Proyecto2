from django import forms
from .models import persona

#Formulario para Crear Personas
class PersonaForm(forms.ModelForm):
   
    class Meta:
        model = persona
        fields = ('nombre','apellido')
        label = {
            
            'nombre':('Nombre de la persona'),
            'apellido':('Apellido de la persona'),
            
        }
        help_texts ={
           
            'nombre':('Campo obligatorio'),
            'apellido':('Campo obligatorio'),
            
        }
class PersonasSistema(forms.Form):
    fields = {'pasaporte'}