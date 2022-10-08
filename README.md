# Antares project
  
## Requisitos  
- Python 3.6 o superiror  
- pip  
- virtualenv  
  
## Como instalar  
  
- Crea un entorno virtualenv y actívalo.  
- Clona el repositorio con:   
  - `git clone https://github.com/hartas17/antares.git`  
- Instala los requerimientos con:   
  - `pip install -r requirements/local.txt`
- Ejecutar migraciones:
	- `python manage.py migrate`
- Crear super usuario para el admin (opcional):
	- `python manage.py createsuperuser`
  
## Como ejecutar
 
    python manage.py runserver --settings antares.settings.local  

 
## Baterías incluidas  
- Django  
- Django rest  
- JWT  
- Rest endpoints para cuentas de usuario con JWT authentication:   
  - Registro con email
  - Activación de cuentas por email (Activado por default)  
  - Inicio de sesión  
  - Restablecimiento de contraseñas con url de un único uso  
  - Cambio de contraseña  
  - Postman Collection  
- Paginación automático con parametro dinámico para tamaño  
- Cuenta de correo temporal configurada (temporal@temp.com)  
  
  
## Validadores genéricos:  
**Nota:** Antes de crear un validador generico y reinventar la rueda revisa los que el framework ya tiene incluidos: [https://docs.djangoproject.com/en/dev/ref/validators/](https://docs.djangoproject.com/en/2.1/ref/validators/)  
  
### Validadores genéricos in house:  
RFC de México  
Códigos de color en hexadecimal (#FFF, #00FF00)  
*Validar peso de archivos o imágenes con parámetros  
*Validación de números telefónicos (10 dígitos)  
*Función para reducir tamaño y peso en imágenes.  
  
### Como utilizar validadores  
  
    from django.db import models from common.validators import validate_rfc
    
           
    class MyModel(models.Model): 
        rfc = models.Charfield(models.CharField(max_length=30, validators=[validate_rfc]))    

## Buenas prácticas:  

### Generales  
- Usar variables de entorno para todo la información sensible, por ejemplo: Contraseñas de servicios, api keys, secret keys, etc.  
- Establecer variables de entorno en los scripts de activar y desactivar del entorno virtual de cada proyecto.  
  
### Django y Django Rest  
- Para usar algún valor del settings utilizar el recomendado por la documentación y no importar el archivo directo.  
- Las validaciones no genéricas, siempre se deben estar en los serializers o forms, nunca en las views o en la sobre escritura del método save() de los modelos.  
  
## Como establecer variables de entorno en Windows  
Para activar y desactivar las variables de entorno de forma automática, es necesario agregar en los archivos que activan y desactivan el entorno virtual de python, en Windows el archivo a editar, si usas PowerShell (recomendado), es el active.ps1 que es el script de para PowerShell:  
  
 

    Set: 
    $env:DJANGO_SETTINGS_MODULE = 'antares.settings.local'     
    
    Delete: 
    Remove-Item env:DJANGO_SETTINGS_MODULE 

 
  
### Como establecer variables de entorno en sistemas Posix en el virtualenv  
  
## Entorno de producción  
- Generar nueva SECRET_KEY siempre, ya que a pesar de que cuando se ejecuta el comando para renombrar el proyecto se genera una nueva secret_key, esta se versiona y puede quedar comprometida.  
```  
from django.core.management.utils import get_random_secret_key  
  
key = get_random_secret_key()  
print(key)  
```
