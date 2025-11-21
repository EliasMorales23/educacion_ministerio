from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from evaluaciones_educativas.models import *
from evaluaciones_educativas.forms.forms import *
from django.db import transaction




def carga_alumno(request):
    alumno_form = AlumnoForm()
    grado_form = GradoForm()
    seccion_form = SeccionForm()
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST)
        grado_form = GradoForm(request.POST)
        seccion_form = SeccionForm(request.POST)
        if alumno_form.is_valid() and grado_form.is_valid() and seccion_form.is_valid():
           #una instancia a la vez
            with transaction.atomic():
                #--------------------logica para no repetir grado---------------
                nombre_grado=grado_form.cleaned_data["nombre_grado"]
                cueanexo_grado=grado_form.cleaned_data["cueanexo"]
                #conseguir cueanexo de v_oferta
                #cueanexo_grado=4
                #turno_grado=grado_form.cleaned_data["turno"]
                
                instancia_grado, creado_grado=Grado.objects.get_or_create(
                    nombre_grado=nombre_grado,
                    cueanexo=cueanexo_grado
                    )
                # print(creado_grado)
                #-----------------logica para no repetir seccion seccion----------
                turno_seccion=seccion_form.cleaned_data["turno"]
                nombre_seccion=seccion_form.cleaned_data["seccion"]
                instancia_seccion, creado_seccion = Seccion.objects.get_or_create(
                seccion=nombre_seccion,
                turno=turno_seccion,
                grado=instancia_grado
                )
                
                alumno = alumno_form.save(commit=False)
                alumno.grado = instancia_grado
                alumno.save()
            return redirect("asistencia", alumno_public_id=alumno.public_id)
            
    context = {
        'alumno_form': alumno_form,
        'grado_form': grado_form,
        'seccion_form': seccion_form,
               }
    return render(request, "alumno.html", context)

def editar_alumno(request,alumno_public_id):
    instancia_alumno=Alumno.objects.get(public_id=alumno_public_id)
    instancia_grado=Grado.objects.get(id=instancia_alumno.grado_id)
    instancia_seccion=Seccion.objects.get(grado_id=instancia_grado.id)
    alumno_form = AlumnoForm(instance=instancia_alumno)
    grado_form = GradoForm(instance=instancia_grado)
    seccion_form = SeccionForm(instance=instancia_seccion)
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST, instance=instancia_alumno)
        grado_form = GradoForm(request.POST, instance=instancia_grado)
        seccion_form = SeccionForm(request.POST, instance=instancia_seccion)
        if alumno_form.is_valid() and grado_form.is_valid() and seccion_form.is_valid():
            nombre_grado=grado_form.cleaned_data["nombre_grado"]
            #turno_grado=grado_form.cleaned_data["turno"]
            cueanexo_grado=grado_form.cleaned_data["cueanexo"]
            instancia_grado, creado_grado=Grado.objects.get_or_create(
                nombre_grado=nombre_grado,
                cueanexo=cueanexo_grado
                )
            
            turno_seccion=seccion_form.cleaned_data["turno"]
            nombre_seccion=seccion_form.cleaned_data["seccion"]
            instancia_seccion, creado_seccion = Seccion.objects.get_or_create(
            seccion=nombre_seccion,
            turno=turno_seccion,
            grado=instancia_grado
            )
            # grado=grado_form.save()
            # seccion=seccion_form.save(commit=False)
            # seccion.grado=grado
            # seccion.save()
            #grado=grado_form.save()
            alumno = alumno_form.save(commit=False)
            alumno.grado = instancia_grado
            alumno.save()
            #alumno= alumno_form.save()
            return redirect("editar_asistencia", alumno_public_id=alumno.public_id)
    context = {
        'alumno_form': alumno_form,
         'grado_form': grado_form,
        'seccion_form': seccion_form,
               }
    return render(request, "alumno.html", context)

def lista(request,grado_public_id):
    #alumnos = Alumno.objects.filter(discapacidad='SI').order_by('nombre')
    #evaluacion = EvaluacionFluidezLectora.objects.filter(asistencia='AUSENTE')
    #grado= Grado.objects.filter(cueanexo=cueanexo).first()
    grado_public=grado_public_id
    grado=Grado.objects.get(public_id=grado_public)
    alumnos = Alumno.objects.filter(grado_id=grado.id).order_by('nombre')
    evaluacion = EvaluacionFluidezLectora.objects.filter(alumno__in=alumnos)
    contexto = {
        'lista_alumnos': alumnos,
        'evaluciones': evaluacion,
    }
    
    return render(request,"lista.html", contexto)#,{"alumnos":alumnos, "query":alumno})
    

def carga_evaluacion(request, alumno_public_id):
    alumno_id=get_object_or_404(Alumno, public_id=alumno_public_id)
    instancia_grado=Grado.objects.get(id=alumno_id.grado_id)
    id_grado=instancia_grado.id
    if request.method == 'POST':
        form = EvaluacionFluidezForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.alumno =alumno_id
            evaluacion.asistencia='PRESENTE'
            evaluacion.save()
            return redirect("lista", Grado=id_grado)
    else:
        #Instancia vacia para metodo get
        form = EvaluacionFluidezForm()
        #Creacion de diccionario para el Post
    context = {'form': form,
               'alumno':alumno_id}
    return render(request, "evaluacion.html", context)


def editar_evaluacion(request, alumno_public_id):
    alumno_id=Alumno.objects.get(public_id=alumno_public_id)
    instancia_grado=Grado.objects.get(id=alumno_id.grado_id)
    #cueanexo=instancia_grado.cueanexo
    grado_public=instancia_grado.public_id
    instancia_evaluacion=EvaluacionFluidezLectora.objects.get(alumno_id=alumno_id.id)
    form=EvaluacionFluidezForm(instance=instancia_evaluacion)
    if request.method == 'POST':
        form=EvaluacionFluidezForm(request.POST,instance=instancia_evaluacion)
        if form.is_valid():
            evaluacion=form.save(commit=False)
            evaluacion.alumno_id = alumno_id
            evaluacion.asistencia='PRESENTE'
            evaluacion.save()
            return redirect("lista", grado_public_id=grado_public)
    context = {'form': form,
               'alumno':alumno_id}
    return render(request, "evaluacion.html", context)


def asistencia(request,alumno_public_id):
    alumno_id=get_object_or_404(Alumno, public_id=alumno_public_id)
    instancia_evaluacion, creando_evaluacion=EvaluacionFluidezLectora.objects.get_or_create(alumno_id=alumno_id.id)
    instancia_grado=Grado.objects.get(id=alumno_id.grado_id)
    #cueanexo=instancia_grado.cueanexo
    grado_public=instancia_grado.public_id
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        
        if form.is_valid():
            asistencia= form.cleaned_data["asistencia"]
            if asistencia: 
                return redirect("carga_evaluacion", alumno_public_id=alumno_id.public_id)
            else:
                #llamamos a funcion ausentismo
                ausentismo_evaluacion(instancia_evaluacion)
                return redirect("lista",grado_public_id=grado_public)
    else:
        form = AsistenciaForm()
    context = {'form': form,
               'alumno':alumno_id
               }
    return render(request,"asistencia.html",context)

def editar_asistencia(request,alumno_public_id):
    #INSTANCIAS
    alumno_id=get_object_or_404(Alumno, public_id=alumno_public_id)
    instancia_grado=Grado.objects.get(id=alumno_id.grado_id)
    #cueanexo=instancia_grado.cueanexo
    grado_public=instancia_grado.public_id
    #manejar error de que no tenga examen, esdecir si carga alumno pero no examen
    #instancia_evaluacion=get_object_or_404(EvaluacionFluidezLectora,alumno_id=alumno_id.id)
    instancia_evaluacion, creando_evaluacion=EvaluacionFluidezLectora.objects.get_or_create(alumno_id=alumno_id.id)
    if request.method == 'POST':
        asistencia_form = AsistenciaForm(request.POST)
        #Campos de tabla evaluacion
        #evaluacion_campos=instancia_evaluacion._meta.fields
        if asistencia_form.is_valid():
            asistencia= asistencia_form.cleaned_data["asistencia"]
            #verificamos alumno presente
            if asistencia: 
                return redirect("editar_evaluacion", alumno_public_id=alumno_id.public_id)
            else:
                #funcion para asuntismo
                
                instancia_evaluacion=ausentismo_evaluacion(instancia_evaluacion)
                instancia_evaluacion.save()
                return redirect("lista",grado_public_id=grado_public)
    else:
        asistencia_form = AsistenciaForm()
    context = {'form': asistencia_form
               }
    return render(request,"asistencia.html",context)


def ausentismo_evaluacion(instancia_evaluacion):
    evaluacion_campos=instancia_evaluacion._meta.fields
    for i in evaluacion_campos:
        if i.name=='asistencia':
            #FUNCION DE PYTHON para estabalecer valores a campos de un objeto
            setattr(instancia_evaluacion, i.name, 'AUSENTE')
            #verificamos campos PK y NOT NULL
        if not i.primary_key and i.null:
            setattr(instancia_evaluacion, i.name, None)
    return instancia_evaluacion