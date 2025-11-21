from django.db import models
import uuid

# Create your models here.

class Grado(models.Model):
    OPCIONES_GRADO = [
    # ('PRIMERO', '1er Grado'),
    ('SEGUNDO', '2do Grado'),
    ('TERCERO', '3er Grado'),
    # ('CUARTO', '4to Grado'),
    # ('QUINTO', '5to Grado'),
    # ('SEXTO', '6to Grado'),
    # ('SEPTIMO', '7mo Grado'),
    ]
    # OPCIONES_TURNO = [
    # ('MANANA', 'Mañana'),
    # ('TARDE', 'Tarde'),
    # ]
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    cueanexo = models.IntegerField()#REPRESENTA A ESCUELA
    nombre_grado = models.CharField(max_length=8, choices= OPCIONES_GRADO, default='SEGUNDO')
    #turno = models.CharField(max_length=6, choices=OPCIONES_TURNO, default='MANANA' )
    class Meta:
       #managed = False
        db_table = 'grados' 
        #unique_together = ('nombre_grado', 'cueanexo')   
    def __str__(self):
        return self.nombre_grado

class Seccion(models.Model):
    OPCIONES_SECCION = [
	('UNICO', 'Unico'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
    ('H', 'H'),
    ('I', 'I'),
    ('J', 'J'),
    ('K', 'K'),
    ]
    OPCIONES_TURNO = [
    ('MANANA', 'Mañana'),
    ('TARDE', 'Tarde'),
    ]
    seccion = models.CharField(max_length=5, choices=OPCIONES_SECCION, default='UNICO')
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    turno = models.CharField(max_length=6, choices=OPCIONES_TURNO, default='MANANA' )
    class Meta:
        #managed = False
        db_table = 'secciones'
        #unicidad
        unique_together = ('seccion', 'grado','turno')
    def __str__(self):
        nombre_seccion=f'{self.grado}_{self.seccion}_{self.turno}'
        return nombre_seccion

class Alumno(models.Model):
    OPCIONES_COMUNIDAD_INDIGENA = [
    ('QOM', 'Qom (Toba)'),
    ('MOQOIT', 'Moqoit (Mocoví)'),
    ('WICHI', 'Wichí (Mataco)'),
    ('NINGUNA', 'Ninguna / No Aplica'),
]
    OPCIONES_DISCAPACIDAD = [
    ('SI', 'Sí, la persona tiene una discapacidad'),
    ('NO', 'No aplica'),
]
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    dni = models.CharField(max_length=9,unique=True,null=True,blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    #cueanexo = models.IntegerField() # Consumiriamos de tabla cuanexo de escuela
    comunidad_indigena=models.CharField(max_length=11, choices= OPCIONES_COMUNIDAD_INDIGENA, default='NINGUNA')
    discapacidad = models.CharField(choices=OPCIONES_DISCAPACIDAD, default='NO')
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    class Meta:
        #managed = False
        db_table = 'alumnos'
    def __str__(self):
        alumno_nombre=f'Alumno:{self.nombre} DNI:{self.dni}'
        return alumno_nombre


class EvaluacionFluidezLectora(models.Model):
    OPCIONES_EVALUACION = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('NORESPONDE', 'NoResponde'),    
	]
    OPCIONES_ASISTENCIA = [
    ('PRESENTE','Presente'),
    ('AUSENTE','Ausente'),    
	]
    cantidad_palabras_leidas = models.IntegerField(default=0, null=True)
    pregunta_1 = models.CharField(max_length=10,choices= OPCIONES_EVALUACION, default='NORESPONDE',null=True)
    pregunta_2 = models.CharField(max_length=10,choices= OPCIONES_EVALUACION, default='NORESPONDE',null=True)
    pregunta_3 = models.CharField(max_length=10,choices= OPCIONES_EVALUACION, default='NORESPONDE',null=True)
    pregunta_4 = models.CharField(max_length=10,choices= OPCIONES_EVALUACION, default='NORESPONDE',null=True)
    pregunta_5 = models.CharField(max_length=10,choices= OPCIONES_EVALUACION, default='NORESPONDE',null=True)
    pregunta_6 = models.CharField(max_length=10,choices= OPCIONES_EVALUACION, default='NORESPONDE',null=True)
    asistencia = models.CharField(choices=OPCIONES_ASISTENCIA,default='AUSENTE')
    alumno = models.OneToOneField(Alumno,primary_key=True, on_delete=models.CASCADE)
    class Meta:
        #managed = False
        db_table = 'evaluaciones_fluidez_lectora'
    def __str__(self):
        nombre_examen=f'Examen fluidez lectora de {self.alumno.nombre}'
        return nombre_examen