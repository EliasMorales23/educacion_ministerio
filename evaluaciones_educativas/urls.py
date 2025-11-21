from django.urls import path
from . import views
# from django.contrib.auth.views import LogoutView



urlpatterns = [
	path('carga_alumno/',views.carga_alumno, name= 'carga_alumno'),
    path('editar_alumno/<uuid:alumno_public_id>/',views.editar_alumno, name= 'editar_alumno'),
	path('carga_evaluacion/<uuid:alumno_public_id>/',views.carga_evaluacion, name= 'carga_evaluacion'),
	path('editar_evaluacion/<uuid:alumno_public_id>/',views.editar_evaluacion, name= 'editar_evaluacion'),
	path('lista/<uuid:grado_public_id>/',views.lista, name='lista'),
	path('asistencia/<uuid:alumno_public_id>/',views.asistencia, name='asistencia'),
	path('editar_asistencia/<uuid:alumno_public_id>/',views.editar_asistencia, name='editar_asistencia'),
	#INCLUIR LA VISTA PARA LOS ADMIN (DONDE VEO SI LAS ESCUELAS ESTAN CARGANDO)
	
]
