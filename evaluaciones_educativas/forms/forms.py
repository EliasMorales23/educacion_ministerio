from django import forms
from evaluaciones_educativas.models import *

class AlumnoForm(forms.ModelForm):

	class Meta:
		model = Alumno
		fields = ['dni','nombre','apellido','comunidad_indigena' ,'discapacidad']
		#widget  para cambiar tipo de campo
		widgets = {
            'dni': forms.TextInput(attrs={
                'required': 'true',          # Hace el campo obligatorio en HTML
                'minlength': '8',           # Restricción de longitud HTML
                'placeholder': 'Ingresa el dni del alumnno',
				'pattern': '[0-9]*'
            }),
			'nombre': forms.TextInput(attrs={
                'required': 'true', 
                'placeholder': 'Ingresa el Nombre del alumnno',
				'pattern': '[a-z]*'
			}),
			'apellido': forms.TextInput(attrs={
                'required': 'true', 
                'placeholder': 'Ingresa el Apellido del alumnno',
				'pattern': '[a-z]*'
			})
			}
		#label para cambiar nombre de campo


class EvaluacionFluidezForm(forms.ModelForm):
	class Meta:
		model= EvaluacionFluidezLectora
		fields=['cantidad_palabras_leidas','pregunta_1','pregunta_2','pregunta_3','pregunta_4' ,'pregunta_5','pregunta_6']
		widgets = {
			'cantidad_palabras_leidas': forms.NumberInput(attrs={
			'min':'0',
			'placeholder':'Ingrese la cantidad de palabras leidas'
			})}

class AsistenciaForm(forms.Form):
	asistencia= forms.BooleanField(label='asistencia', required=False)

class GradoForm(forms.ModelForm):
	class Meta:
		model = Grado
		fields='__all__'
		#ocultamos cueanexo
		# widgets = {
		# 	'cueanexo': forms.HiddenInput(),
		# 	}
	#solucion para evitar no seleccionar un unique desde el form	

		


class SeccionForm(forms.ModelForm):
	class Meta:
		model = Seccion
		fields=['seccion','turno']