from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from evaluaciones_educativas.models import *
from evaluaciones_educativas.forms.forms import *
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import date, datetime
from openpyxl import Workbook
import psycopg2
import os


@login_required
def carga_alumno(request,grado_public_id):
    grado=get_object_or_404(Grado,public_id= grado_public_id)
    alumno_form = AlumnoForm()
    grado_form = GradoForm(instance=grado)
    seccion_form = SeccionForm()
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST)
        grado_form = GradoForm(request.POST)
        seccion_form = SeccionForm(request.POST)
        if alumno_form.is_valid() and grado_form.is_valid() and seccion_form.is_valid():
           #una instancia a la vez
            with transaction.atomic():
                turno_seccion=seccion_form.cleaned_data["turno"]
                nombre_seccion=seccion_form.cleaned_data["seccion"]
                instancia_seccion, creado_seccion = Seccion.objects.get_or_create(
                seccion=nombre_seccion,
                turno=turno_seccion,
                grado=grado
                )
                
                alumno = alumno_form.save(commit=False)
                alumno.seccion = instancia_seccion
                alumno.save()
                instancia_evaluacion, creando_evaluacion=EvaluacionFluidezLectora.objects.get_or_create(
                alumno_id=alumno.id,cantidad_palabras_leidas=None, pregunta_1=None, pregunta_2=None, pregunta_3=None, pregunta_4=None, pregunta_5=None, pregunta_6=None, asistencia='AUSENTE',encargado_carga='APLICADOR')
            return redirect("asistencia", alumno_public_id=alumno.public_id)
            
    context = {
        'alumno_form': alumno_form,
        'grado_form': grado_form,
        'seccion_form': seccion_form,
        'grado_public':grado_public_id,
               }
    return render(request, "alumno.html", context)

@login_required
def editar_alumno(request,alumno_public_id):
    instancia_alumno=get_object_or_404(Alumno,public_id=alumno_public_id)
    instancia_seccion=get_object_or_404(Seccion,id=instancia_alumno.seccion_id)
    instancia_grado=get_object_or_404(Grado,id=instancia_seccion.grado_id)
    alumno_form = AlumnoForm(instance=instancia_alumno)
    seccion_form = SeccionForm(instance=instancia_seccion)
    grado_form = GradoForm(instance=instancia_grado)
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST, instance=instancia_alumno)
        grado_form = GradoForm(request.POST, instance=instancia_grado)
        seccion_form = SeccionForm(request.POST, instance=instancia_seccion)
        if alumno_form.is_valid() and grado_form.is_valid() and seccion_form.is_valid():
            with transaction.atomic():
                nombre_grado=grado_form.cleaned_data["nombre_grado"]
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
                alumno = alumno_form.save(commit=False)
                alumno.seccion = instancia_seccion
                alumno.save()
            return redirect("editar_asistencia", alumno_public_id=alumno.public_id)
    context = {
        'alumno_form': alumno_form,
         'grado_form': grado_form,
        'seccion_form': seccion_form,
        'grado_public':instancia_grado.public_id,
               }
    return render(request, "alumno.html", context)

@login_required
def lista(request,grado_public_id): 
    instancia_grado=get_object_or_404(Grado,public_id=grado_public_id)
    instancia_seccion=Seccion.objects.filter(grado_id=instancia_grado)
    alumnos = Alumno.objects.filter(seccion_id__in=instancia_seccion).order_by('nombre')
    evaluacion = EvaluacionFluidezLectora.objects.filter(alumno__in=alumnos)
    contexto = {
        'lista_alumnos': alumnos,
        'evaluciones': evaluacion,
        'nombre_grado':instancia_grado.nombre_grado,
        'grado_public_id':instancia_grado.public_id
    }
    return render(request,"lista.html", contexto)
#-----------------lista para grados------------------
@login_required
def lista_grado(request,grado): 
    #---------logica para obtener cueanexo por medio de username--------------
    usuario= request.user
    if usuario.is_authenticated:
        name=usuario.username
    #-----logica para DNI+CUEANEXO---------
    if len(name)>9  and len(name)<=17:
        #DNI+CUEANEXO
        nombre_usuario_cueanexo=name[8:]
    else:
        nombre_usuario_cueanexo=name
    #cueanexo=int(nombre_usuario_cueanexo)   
#-----logica para DNI+CUEANEXO---------
    if grado =='SEGUNDO':
        grado='2do Año/Grado'
    elif grado =='TERCERO':
            grado='3er Año/Grado'
    try:
        instancia_grado=Grado.objects.get(cueanexo=nombre_usuario_cueanexo, nombre_grado=grado)
        return redirect("lista", grado_public_id=instancia_grado.public_id)
    except Grado.DoesNotExist:
        return render(request,"lista.html")
    
@login_required
def grado(request):
    usuario= request.user
    if usuario.is_authenticated:
        name=usuario.username
        #-----logica para DNI+CUEANEXO---------
        if len(name)>9  and len(name)<=17:
            #DNI+CUEANEXO
            nombre_usuario_cueanexo=name[8:]
        else:
            nombre_usuario_cueanexo=name
        #cueanexo=int(nombre_usuario_cueanexo)
        #-----logica para DNI+CUEANEXO---------
        
    opciones_grado = [
                     ('2do Año/Grado', '2do Año/Grado'),
                      ('3er Año/Grado','3er Año/Grado')
                        ]
    grado_form_data = GradoViewForm()
    if request.method == 'POST':
        grado_form_data = GradoViewForm(request.POST)
        grado_form_data.fields['grado'].choices = opciones_grado
        if grado_form_data.is_valid():
            with transaction.atomic():
                grado=grado_form_data.cleaned_data["grado"]
                instancia_grado, creado_grado=Grado.objects.get_or_create(
                    nombre_grado=grado,
                    cueanexo=nombre_usuario_cueanexo
                    )
                grado_public=instancia_grado.public_id
            return redirect("carga_alumno", grado_public_id=grado_public)
    else:
        grado_form_data.fields['grado'].choices = opciones_grado
    contexto = {
        'grado_form_data': grado_form_data
    }
    return render(request,"grados.html", contexto)

    
@login_required
def carga_evaluacion(request, alumno_public_id):
    alumno_id=get_object_or_404(Alumno, public_id=alumno_public_id)
    instancia_seccion=get_object_or_404(Seccion,id=alumno_id.seccion_id)
    instancia_grado=get_object_or_404(Grado,id=instancia_seccion.grado_id)
    grado_public=instancia_grado.public_id
    # print(instancia_grado.nombre_grado)
    if instancia_grado.nombre_grado =='SEGUNDO':
        cantidad_palabra_maxima=170
    else:
        cantidad_palabra_maxima=211

    evaluacion_existente = None
    try:
        # Buscamos el examen que se creó previamente con get_or_create
        # ASUMO que tu modelo se llama EvaluacionFluidezLectora
        evaluacion_existente = EvaluacionFluidezLectora.objects.get(alumno=alumno_id.id)
    except EvaluacionFluidezLectora.DoesNotExist:
        # Si no existe, el formulario será de CREACIÓN (INSERT)
        pass
    if request.method == 'POST':
        form = EvaluacionFluidezForm(request.POST, max_cantidad_palabra=cantidad_palabra_maxima, instance=evaluacion_existente)
        if form.is_valid():
            with transaction.atomic():
                evaluacion = form.save(commit=False)
                evaluacion.alumno = alumno_id
                evaluacion.asistencia ='PRESENTE'
                evaluacion.encargado_carga='APLICADOR'
                evaluacion.save()
            return redirect("lista", grado_public_id=grado_public)
    else:
        #Instancia vacia para metodo get
        form = EvaluacionFluidezForm(max_cantidad_palabra=cantidad_palabra_maxima)
        #Creacion de diccionario para el Post
    context = {'form': form,
               'alumno':alumno_id}
    return render(request, "evaluacion.html", context)

@login_required
def editar_evaluacion(request, alumno_public_id):
    alumno_id=get_object_or_404(Alumno,public_id=alumno_public_id)
    instancia_seccion=get_object_or_404(Seccion,id=alumno_id.seccion_id)
    instancia_grado=get_object_or_404(Grado,id=instancia_seccion.grado_id)
    grado_public=instancia_grado.public_id
    instancia_evaluacion=get_object_or_404(EvaluacionFluidezLectora,alumno_id=alumno_id.id)
    if instancia_grado.nombre_grado =='SEGUNDO':
        cantidad_palabra_maxima=170
    else:
        cantidad_palabra_maxima=211
    form=EvaluacionFluidezForm(instance=instancia_evaluacion, max_cantidad_palabra=cantidad_palabra_maxima)
    if request.method == 'POST':
        form=EvaluacionFluidezForm(request.POST,instance=instancia_evaluacion,max_cantidad_palabra=cantidad_palabra_maxima)
        if form.is_valid():
            with transaction.atomic():
                evaluacion=form.save(commit=False)
                evaluacion.alumno_id = alumno_id
                evaluacion.asistencia='PRESENTE'
                evaluacion.encargado_carga='APLICADOR'
                evaluacion.save()
            return redirect("lista", grado_public_id=grado_public)
    context = {
        'form': form,
        'alumno':alumno_id
        }
    return render(request, "evaluacion.html", context)

@login_required
def asistencia(request,alumno_public_id):
    alumno_id=get_object_or_404(Alumno, public_id=alumno_public_id)
     #SI instanciamos aca recibe la evalaucion que se creo en carga...
    instancia_evaluacion=get_object_or_404(EvaluacionFluidezLectora, alumno_id=alumno_id.id) 
    instancia_seccion=get_object_or_404(Seccion,id=alumno_id.seccion_id)
    instancia_grado=get_object_or_404(Grado,id=instancia_seccion.grado_id)
    grado_public=instancia_grado.public_id
    if request.method == 'POST':
            form = AsistenciaForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    asistencia= form.cleaned_data["asistencia"]
                    if asistencia: 
                        return redirect("carga_evaluacion", alumno_public_id=alumno_id.public_id)
                    else:
                        #llamamos a funcion ausentismo
                        evaluacion=ausentismo_evaluacion(instancia_evaluacion)
                        evaluacion.save()
                        return redirect("lista", grado_public_id=grado_public)
    else:
        form = AsistenciaForm()
    context = {'form': form,
               'alumno':alumno_id
               }
    return render(request,"asistencia.html",context)

@login_required
def editar_asistencia(request,alumno_public_id):
    #INSTANCIAS
    alumno_id=get_object_or_404(Alumno, public_id=alumno_public_id)
    instancia_seccion=get_object_or_404(Seccion,id=alumno_id.seccion_id)
    instancia_grado=get_object_or_404(Grado,id=instancia_seccion.grado_id)
    grado_public=instancia_grado.public_id
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        #Campos de tabla evaluacion
        if form.is_valid():
            with transaction.atomic():
                asistencia = form.cleaned_data["asistencia"]
                #verificamos alumno presente
                if asistencia: 
                    return redirect("editar_evaluacion", alumno_public_id=alumno_id.public_id)
                else:
                    #Recien instanciamos en el ELSE 
                    instancia_evaluacion=get_object_or_404(EvaluacionFluidezLectora, alumno_id=alumno_id.id)
                    evaluacion=ausentismo_evaluacion(instancia_evaluacion)
                    evaluacion.save()
                    return redirect("lista", grado_public_id=grado_public)
    else:
        asistencia_form = AsistenciaForm()
    context = {'form': asistencia_form}
    return render(request,"asistencia.html",context)

@login_required
def borrar_registro_alumno(request,alumno_public_id):
    alumno_id=get_object_or_404(Alumno, public_id=alumno_public_id)
    instancia_seccion=get_object_or_404(Seccion,id=alumno_id.seccion_id)
    instancia_grado=get_object_or_404(Grado,id=instancia_seccion.grado_id)
    grado_public=instancia_grado.public_id
    if request.method == 'POST':
        form = BorrarRegistroAlumnoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                eleccion= form.cleaned_data["borrar"]
                if eleccion:
                    alumno_id.delete()
                    return redirect("lista_filtro_monitoreo")
                else:
                    return redirect("lista_filtro_monitoreo")
    else:
        form = BorrarRegistroAlumnoForm()
    context = {'form': form,
               'alumno':alumno_id
               }
    return render(request,"borrar_registro_alumno.html",context)

@login_required
def descargar_excel(request,grado_public_id):
    instancia_grado=get_object_or_404(Grado,public_id=grado_public_id)
    instancia_seccion=Seccion.objects.filter(grado_id=instancia_grado)
    alumnos = Alumno.objects.filter(seccion_id__in=instancia_seccion).order_by('nombre')
    evaluacion = EvaluacionFluidezLectora.objects.filter(alumno__in=alumnos)
    # 1. Configurar la respuesta HTTP para un archivo Excel
    # El 'mimetype' (o Content-Type) es crucial para que el navegador sepa que es un archivo .xlsx
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    
    # 2. Configurar el encabezado Content-Disposition
    # Esto le dice al navegador que DEBE descargar el contenido y le asigna un nombre de archivo.
    if instancia_grado.nombre_grado=='2do Año/Grado':
        nombre_grado='2do_Grado_'
    elif instancia_grado.nombre_grado=='3er Año/Grado':
        nombre_grado='3er_Grado_'
    else:
        nombre_grado='_'
    response['Content-Disposition'] = f'attachment; filename="reporte_fluidez_{nombre_grado}noviembre_2025.xlsx"'

    # 3. Generar el contenido del Excel (lo mismo que tenías)
    wb = Workbook()
    ws = wb.active
    fecha_hora_actual = datetime.now()
    ws['A1'] = f'CUEANEXO: {instancia_grado.cueanexo}'
    ws['G1'] = f'FECHA Y HORA:  {fecha_hora_actual.strftime("%d/%m/%Y %I:%M:%S %p")}'
    lista=['NOMBRE','APELLIDO','DNI','COMUNIDAD INDíGENA','DISCAPACIDAD','GRADO','SECCIÓN','TURNO','ASISTENCIA','FLUIDEZ','P1','P2','P3','P4','P5','P6']
    #print(alumnos)
    ws.append(lista)
    for i,v in enumerate(evaluacion):
        ws[f'A{i + 3}']=v.alumno.nombre
        ws[f'B{i + 3}']=v.alumno.apellido
        ws[f'C{i + 3}']=v.alumno.dni
        ws[f'D{i + 3}']=v.alumno.comunidad_indigena
        ws[f'E{i + 3}']=v.alumno.discapacidad
        ws[f'F{i + 3}']=v.alumno.seccion.grado.nombre_grado
        ws[f'G{i + 3}']=v.alumno.seccion.seccion
        ws[f'H{i + 3}']=v.alumno.seccion.turno
        ws[f'I{i + 3}']=v.asistencia
        ws[f'J{i + 3}']=v.cantidad_palabras_leidas
        ws[f'K{i + 3}']=v.pregunta_1
        ws[f'L{i + 3}']=v.pregunta_2
        ws[f'M{i + 3}']=v.pregunta_3
        ws[f'N{i + 3}']=v.pregunta_4
        ws[f'O{i + 3}']=v.pregunta_5
        ws[f'P{i + 3}']=v.pregunta_6

    wb.save(response)
    # 5. Retornar la respuesta al navegador
    return response

# @login_required
# def monitoreo(request):
#     instancia_grado_cueanexo=Grado.objects.all()
#     # instancia_grado=Grado.objects.filter(cueanexo__in=instancia_grado_cueanexo).values_list('nombre_grado',flat=True)
#     # # for i in instancia_grado:
#     # #     print(i)
#     contexto={'grados':instancia_grado_cueanexo}
#     return render(request,"monitoreo.html", contexto)

#---------------------------------------------------------
@login_required
def filtro_monitoreo(request): 
    alumno = None
    evaluacion=None
    if request.method == 'POST':
        #form_cueanexo = CueanexoViewForm(request.POST)
        form_dni= DniViewForm(request.POST)
        if form_dni.is_valid():
            with transaction.atomic():
                # cueanexo= form_cueanexo.cleaned_data["cueanexo"]
                dni= form_dni.cleaned_data["dni"] 
                # instancia_grado=Grado.objects.filter(cueanexo__in=cueanexo)
                # instancia_seccion=get_object_or_404(Seccion,grado_id=instancia_grado)
                try: 
                    alumno = Alumno.objects.get(dni=dni)
                    print(alumno)
                    evaluacion = EvaluacionFluidezLectora.objects.get(alumno=alumno)
                    print(evaluacion)
                except Alumno.DoesNotExist:
                    alumno = 'vacio' # No encontró el alumno
                except EvaluacionFluidezLectora.DoesNotExist:
                    evaluacion = 'vacio' # Encontró el alumno, pero no la evalua
                    print(evaluacion)

    else:           
        # form_cueanexo = CueanexoViewForm()
        form_dni = DniViewForm()
    contexto = {
        'alumno':alumno,
        'form_dni': form_dni,
        'evaluacion':evaluacion}
    return render(request,"lista_filtro_monitoreo.html",contexto)


#-------------SE AÑADE MONITOREO PARA ESTABLECIMIIENTOS-----------------------------------
@login_required
def monitoreo_establecimientos_sin_carga(request):
    lista=[]
    resultados=None
    try:
        conn=psycopg2.connect(host=os.environ.get('POSTGRES_HOST_EVALUACION'), database=os.environ.get('POSTGRES_DB_EVALUACION'), user=os.environ.get('POSTGRES_USER_EVALUACION'), password=os.environ.get('POSTGRES_PASSWORD_EVALUACION'))
        with conn:
            with conn.cursor() as cur:
                print('consultando')
                consulta=f"""SELECT
                                    e.cueanexo,
                                    e.escuela,
                                    e.sector,
                                    e.ambito,
                                    e.region,
                                    e.localidad,
                                    e.departamento,
                                    g.grado_anio
                                FROM public.grados_ministerio g
                                INNER JOIN public.establecimientos_ministerio e
                                    ON g.cueanexo = e.cueanexo
                                WHERE not EXISTS (
                                    SELECT 1
                                    FROM public.grados gr
                                    WHERE gr.cueanexo = e.cueanexo
                                    AND gr.nombre_grado = g.grado_anio
                                )order by e.cueanexo;"""
                cur.execute(consulta)
                resultados=cur.fetchall()
                #print(resultados)
                print("Consulta ejecutada correctamente.")
    except Exception as e:
    # Si hay un error, el bloque 'with conn' hace conn.rollback()
        print(f"Error, se hizo rollback: {e}")
    
    for i in resultados:
        resultados_dict={
        'CUEANEXO':i[0],
        'ESCUELA':i[1],
        'SECTOR':i[2],
        'AMBITO':i[3],
        'REGION':i[4],
        'LOCALIDAD':i[5],
        'DEPARTAMENTO':i[6],
        'GRADO':i[7]
        }  
        lista.append(resultados_dict)
    
    contexto={
        'resultados_consulta':lista,
        'carga':'SIN CARGA'
    }
    if request.method == "POST":
        wb=descargar_excel_monitoreo(lista)
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            'attachment; filename="reporte_carga_establecimientos_Sin_Carga_noviembre_2025.xlsx"'
        )

        wb.save(response)
        return response
        #return render(request, "monitoreo_establecimientos.html",contexto)
    #Enviarlos a la consulta como parametro en la consulta completa a la base
    #para traer todos los establecimeitnos que no cargaron nada 
    return render(request,"monitoreo_establecimientos.html", contexto)

@login_required
def monitoreo_establecimientos_carga(request):
    lista=[]
    resultados=None
    try:
        conn=psycopg2.connect(host=os.environ.get('POSTGRES_HOST_EVALUACION'), database=os.environ.get('POSTGRES_DB_EVALUACION'), user=os.environ.get('POSTGRES_USER_EVALUACION'), password=os.environ.get('POSTGRES_PASSWORD_EVALUACION'))
        with conn:
            with conn.cursor() as cur:
                print('consultando')
                consulta=f"""SELECT
                                    e.cueanexo,
                                    e.escuela,
                                    e.sector,
                                    e.ambito,
                                    e.region,
                                    e.localidad,
                                    e.departamento,
                                    g.grado_anio
                                FROM public.grados_ministerio g
                                INNER JOIN public.establecimientos_ministerio e
                                    ON g.cueanexo = e.cueanexo
                                WHERE EXISTS (
                                    SELECT 1
                                    FROM public.grados gr
                                    WHERE gr.cueanexo = e.cueanexo
                                    AND gr.nombre_grado = g.grado_anio
                                )order by e.cueanexo; """
                cur.execute(consulta)
                resultados=cur.fetchall()
                #print(resultados)
                print("Consulta ejecutada correctamente.")
    except Exception as e:
    # Si hay un error, el bloque 'with conn' hace conn.rollback()
        print(f"Error, se hizo rollback: {e}")
    
    for i in resultados:
        resultados_dict={
        'CUEANEXO':i[0],
        'ESCUELA':i[1],
        'SECTOR':i[2],
        'AMBITO':i[3],
        'REGION':i[4],
        'LOCALIDAD':i[5],
        'DEPARTAMENTO':i[6],
        'GRADO':i[7]
        }  
        lista.append(resultados_dict)
    contexto={
        'resultados_consulta':lista,
        'carga':'CON CARGAS'
    }
    if request.method == "POST":
        wb=descargar_excel_monitoreo(lista)
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            'attachment; filename="reporte_carga_establecimientos_Cargados_noviembre_2025.xlsx"'
        )

        wb.save(response)
        return response
    #Enviarlos a la consulta como parametro en la consulta completa a la base
    #para traer todos los establecimeitnos que no cargaron nada 
    return render(request,"monitoreo_establecimientos.html", contexto)
#------------------------------------------------------------
#DESCARGA DE MONITOREO
def descargar_excel_monitoreo(resultados):
    
    # 3. Generar el contenido del Excel (lo mismo que tenías)
    wb = Workbook()
    ws = wb.active
    fecha_hora_actual = datetime.now()
    #ws['A1'] = f'CUEANEXO: {instancia_grado.cueanexo}'
    ws['A1'] = f'FECHA Y HORA:  {fecha_hora_actual.strftime("%d/%m/%Y %I:%M:%S %p")}'
    lista=['CUEANEXO','ESCUELA','SECTOR','ÁMBITO','REGIÓN','LOCALIDAD','DEPARTAMENTO','GRADO']
    #print(alumnos)
    ws.append(lista)
    #print(resultados)
    # print(type(resultados))
    # print(resultados[1]['CUEANEXO'])
    for i,v in enumerate(resultados):
        ws[f'A{i + 2}']=resultados[i]['CUEANEXO']
        ws[f'B{i + 2}']=resultados[i]['ESCUELA']
        ws[f'C{i + 2}']=resultados[i]['SECTOR']
        ws[f'D{i + 2}']=resultados[i]['AMBITO']
        ws[f'E{i + 2}']=resultados[i]['REGION']
        ws[f'F{i + 2}']=resultados[i]['LOCALIDAD']
        ws[f'G{i + 2}']=resultados[i]['DEPARTAMENTO']
        ws[f'H{i + 2}']=resultados[i]['GRADO']
    
    
    # 5. Retornar la respuesta al navegador
    return wb

#--------------------------------------------------------

def ausentismo_evaluacion(instancia_evaluacion):
    evaluacion_campos=instancia_evaluacion._meta.fields
    for i in evaluacion_campos:
        if i.name == 'asistencia':
            #FUNCION DE PYTHON para estabalecer valores a campos de un objeto
            setattr(instancia_evaluacion, i.name, 'AUSENTE')
            #verificamos campos PK y NOT NULL
        if not i.primary_key and i.null:
            setattr(instancia_evaluacion, i.name, None)
    return instancia_evaluacion

@login_required
def inicio_aplicador(request):
    return render(request,"header_director.html")

#logica de logue--BORRAR-------------------
def salir(request):
    logout(request)
    return redirect('lista_filtro_monitoreo')
#-----------------------------


@login_required
def borrar_registro_alumno_sin_evaluacion(request,alumno_public_id):
    alumno = get_object_or_404(Alumno, public_id=alumno_public_id)

    # 2. Borrar el registro
    alumno.delete()
    
    # 3. ¡IMPORTANTE! Devolver la redirección.
    #    'lista_filtro_monitoreo' debe ser el *nombre* de la URL en tu urls.py
    return redirect('lista_filtro_monitoreo')