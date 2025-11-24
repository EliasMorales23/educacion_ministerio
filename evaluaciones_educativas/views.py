from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from evaluaciones_educativas.models import *
from evaluaciones_educativas.forms.forms import *
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def carga_alumno(request):
    #def carga_alumno(request, cuaenexo/usuario):
    #---------logica para obtener cueanexo por medio de username--------------
    usuario= request.user
    if usuario.is_authenticated:
        nombre_usuario_cueanexo=usuario.username
        valor_inicial={'cueanexo': nombre_usuario_cueanexo}
        # print(nombre_usuario_cueanexo)
        # print(type(nombre_usuario_cueanexo))
    #--------------------------------------------------------------------
    alumno_form = AlumnoForm()
    grado_form = GradoForm(initial=valor_inicial)
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
                #cueanexo_grado=grado_form.cleaned_data["cueanexo"]#01
                #conseguir cueanexo de v_oferta
                #cueanexo_grado=4 ACA ES DONDE PSARIAMOS EL CUEANEXO O USUARIO EN LUGAR DE 01
                #la idea es hacerlo con un TRY para si es de 9 digiots entender que es el cueanexo 
                #y si es 18 ennder que es el dni+cueanexo

                
                instancia_grado, creado_grado=Grado.objects.get_or_create(
                    nombre_grado=nombre_grado,
                    cueanexo=nombre_usuario_cueanexo
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

def lista(request,seccion_id, eleccion):
    #-------------------
    print(seccion_id)
    seccion=Seccion.objects.get(id=seccion_id, turno=eleccion)
    print(seccion.grado_id)
    instancia_grado=Grado.objects.get(id=seccion.grado_id)
    #----------------------------------
    # consulta=Alumno.objects.filter(
    #     grado__
    #     seccion__


    # )
    #---------------------
    grado_public=instancia_grado.public_id
    grado=Grado.objects.get(public_id=grado_public)
    alumnos = Alumno.objects.filter(grado_id=grado.id).order_by('nombre')
    evaluacion = EvaluacionFluidezLectora.objects.filter(alumno__in=alumnos)
    contexto = {
        'lista_alumnos': alumnos,
        'evaluciones': evaluacion,
    }
    return render(request,"lista.html", contexto)#,{"alumnos":alumnos, "query":alumno})
#-----------grado y secciom-------------------------------------
@login_required
def grado(request):
    usuario= request.user
    if usuario.is_authenticated:
        nombre_usuario_cueanexo=usuario.username
        cueanexo=nombre_usuario_cueanexo
    instancia_grado= Grado.objects.filter(cueanexo=cueanexo)

    #print(cueanexo)
    opciones_grado = [('', '-- Elige un Grado --')]
    #print(instancia_grado.get('nombre_grado'))
    for grado in instancia_grado:
        opciones_grado.append((grado.id, grado.nombre_grado))
    #print(opciones_grado['nombre_grado'])
    # 3. Inicializar el formulario
    grado_form_data = GradoViewForm()
    
    # 4. Asignar las opciones al campo 'seccion'
    #grado_form.fields['grado'].choices = opciones_grado
    if request.method == 'POST':
        grado_form_data = GradoViewForm(request.POST)
        grado_form_data.fields['grado'].choices = opciones_grado
        if grado_form_data.is_valid():
            with transaction.atomic():
                grado_id=grado_form_data.cleaned_data["grado"]
                grado=instancia_grado.get(cueanexo=cueanexo,id=grado_id)
                grado_public=grado.public_id
                return redirect("secciones", grado_public_id=grado_public)
    else:
        grado_form_data.fields['grado'].choices = opciones_grado
    contexto = {
        'grado_form_data': grado_form_data
    }
    return render(request,"grados.html", contexto)

def seccion(request, grado_public_id):
    instancia_grado=Grado.objects.get(public_id=grado_public_id)
    instancia_seccion=Seccion.objects.filter(grado_id=instancia_grado)
    opciones_seccion = [('', '-- Elige una Sección --')] # El empty_label va primero
    
    # Suponiendo que tu modelo Seccion tiene 'id' y 'nombre'
    for seccion in instancia_seccion:
        opciones_seccion.append((seccion.id, seccion.seccion))
        
    # 3. Inicializar el formulario
    form = SeccionViewForm()
    if request.method == 'POST':
        form = SeccionViewForm(request.POST)
        form.fields['seccion'].choices = opciones_seccion
        if form.is_valid():
            with transaction.atomic():
                seccion_id=form.cleaned_data["seccion"]
                seccion=instancia_seccion.get(id=seccion_id)
                return redirect("turnos", seccion_id=seccion.id)
    else:
        form.fields['seccion'].choices = opciones_seccion
    
    # # 4. Asignar las opciones al campo 'seccion'
    # form.fields['seccion'].choices = opciones_seccion
    contexto = {
        'form': form
    }
    return render(request,"secciones.html", contexto)#,{"alumnos":alumnos, "query":alumno})



def turno(request, seccion_id):
    # instancia_grado=Grado.objects.get(public_id=grado_public_id)
    instancia_seccion=Seccion.objects.filter(id=seccion_id)
    opciones_turno = [('', '-- Elige un Turno --')] # El empty_label va primero
    
    # # Suponiendo que tu modelo Seccion tiene 'id' y 'nombre'
    for seccion in instancia_seccion:
         opciones_turno.append((seccion.id, seccion.turno))
        
    # # 3. Inicializar el formulario
    form = TurnoViewForm()
    if request.method == 'POST':
        form = TurnoViewForm(request.POST)
        form.fields['turno'].choices = opciones_turno
        if form.is_valid():
            with transaction.atomic():
                seccion_id=form.cleaned_data["turno"]
                int_seccion_id=int(seccion_id)
                # print(type(seccion_id))
                # print(opciones_turno)
                eleccion= [v for k,v in opciones_turno if k == int_seccion_id][0]
                print(eleccion)
                print('------')
                seccion=instancia_seccion.get(id=seccion_id)
                print(seccion.grado_id)
                instancia_grado=Grado.objects.get(id=seccion.grado_id)
                return redirect("lista", seccion_id=seccion.id, turno=eleccion)
    else:
        form.fields['turno'].choices = opciones_turno
    
    contexto = {
        'form': form
    }
    return render(request,"turnos.html", contexto)#,{"alumnos":alumnos, "query":alumno})
#---------------------------------------------------------
    

def carga_evaluacion(request, alumno_public_id):
    alumno_id=get_object_or_404(Alumno, public_id=alumno_public_id)
    instancia_grado=Grado.objects.get(id=alumno_id.grado_id)
    grado_public=instancia_grado.public_id
    if request.method == 'POST':
        form = EvaluacionFluidezForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.alumno =alumno_id
            evaluacion.asistencia='PRESENTE'
            evaluacion.save()
            return redirect("lista", grado_public_id=grado_public)
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
    #SI instanciamos aca se crea antes de que confirme asistencia (puede ser conveniente)...
    instancia_evaluacion, creando_evaluacion=EvaluacionFluidezLectora.objects.get_or_create(
        alumno_id=alumno_id.id)
    instancia_grado=Grado.objects.get(id=alumno_id.grado_id)
    # #cueanexo=instancia_grado.cueanexo
    grado_public=instancia_grado.public_id
    if request.method == 'POST':
        #----------LOGICA PARA EVALUACION (asistencia seleccionada)---------
    #     instancia_evaluacion, creando_evaluacion=EvaluacionFluidezLectora.objects.get_or_create(
    #     alumno_id=alumno_id.id)
    #     instancia_grado=Grado.objects.get(id=alumno_id.grado_id)
    # #cueanexo=instancia_grado.cueanexo
    #     grado_public=instancia_grado.public_id
        #----------------------------------------
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

#logica de logue----------------------
def salir(request):
    logout(request)
    return redirect('accounts/login.html')
#-----------------------------