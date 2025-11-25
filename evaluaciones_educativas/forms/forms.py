from django import forms
from evaluaciones_educativas.models import *


class GradoViewForm(forms.Form):
	grado= forms.ChoiceField(label='grados', required=False)

class SeccionViewForm(forms.Form):
	seccion= forms.ChoiceField(label='secciones', required=False)
	
class TurnoViewForm(forms.Form):
	turno= forms.ChoiceField(label='Turnos', required=False)

class AlumnoForm(forms.ModelForm):

	class Meta:
		model = Alumno
		fields = ['dni','nombre','apellido','comunidad_indigena' ,'discapacidad']
		#widget  para cambiar tipo de campo
		widgets = {
            'dni': forms.TextInput(attrs={
                'required': 'true',         
                'minlength': '8',
				'maxlength':'8',
                'placeholder': 'INGRESA EL DNI DEL ALUMNO',
				'pattern': '[0-9]*'
            }),
			'nombre': forms.TextInput(attrs={
                'required': 'true', 
                'placeholder': 'NOMBRE DEL ALUMNO EN MAYUSCULA',
				'pattern': '[A-ZÑÁÉÍÓÚ ]*'
			}),
			'apellido': forms.TextInput(attrs={
                'required': 'true', 
                'placeholder': 'APELLIDO DEL ALUMNO EN MAYUSCULA',
				'pattern': '[A-ZÑÁÉÍÓÚ ]*'
			})
			}
		#label para cambiar nombre de campo

class AsistenciaForm(forms.Form):
	asistencia= forms.BooleanField(label='asistencia', required=False)

class EvaluacionFluidezForm(forms.ModelForm):
	class Meta:
		model= EvaluacionFluidezLectora
		fields=['cantidad_palabras_leidas','pregunta_1','pregunta_2','pregunta_3','pregunta_4' ,'pregunta_5','pregunta_6']
		widgets = {
			'cantidad_palabras_leidas': forms.NumberInput(attrs={
			'min':'0',
			'placeholder':'INGRESA LA CANTIDAD DE PALABRAS LEIDAS'
			})}

class GradoForm(forms.ModelForm):
	class Meta:
		model = Grado
		fields=['nombre_grado','cueanexo']
		#ocultamos cueanexo
		widgets = {
			'cueanexo': forms.NumberInput(
				attrs={
					'readonly':'readonly'
				}
			),
			}
	#solucion para evitar no seleccionar un unique desde el form	


class SeccionForm(forms.ModelForm):
	class Meta:
		model = Seccion
		fields=['seccion','turno']