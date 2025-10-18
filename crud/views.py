from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

# se renderiza la pagina home del crud
def home(request):
    return render(request,'home_crud.html')

# se renderiza la pagina de registro de usuario 
def signup(request):
    # Si la pagina envia un metodo GET se renderiza la pagina
    if request.method == 'GET':
        return render(request,'user/signup_crud.html',{
        'form':UserCreationForm, #Nos da un formulario de LOGIN
    })
    # Si la pagina envia un metodo POST se sigue la logica para registrar al usuario
    else:
        #Tomamos los valores enviados por el usuario desde el formulario
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        username = request.POST['username']

        # si ambas contrasenas coinciden intentamos hacer el registro del usuario
        if password1 == password2:
            #register user
            try:
                #creamos una instancia de usuario con una Clase User traida desde models.User
                user = User.objects.create_user(username = username,password=password1)
                #Guardamos al usuario en la base de datos
                user.save()
                #Guardamos la autenticacion del usuario, pasandole request y la instancia del usuario
                login(request,user)
                return redirect('tasks_crud')
            #Manejamos un error en caso de no poder guardarlo
            except IntegrityError:
                return render(request,'user/signup_crud.html',{
                    'form':UserCreationForm, #Nos da un formulario de LOGIN
                    'error':'Username already exists'
                }) 
        #si las  contrasenas no hacen match, se manda un error por pantalla  
        else:
             return render(request,'user/signup_crud.html',{
                    'form':UserCreationForm, #Nos da un formulario de LOGIN
                    'error':'Password do not match'
                })

# se renderiza la pagina de login de usuario 
def signin(request):
    # Si la pagina envia un metodo GET se renderiza la pagina
    if request.method == 'GET':
        return render(request,'user/login_crud.html',{
            'form':AuthenticationForm
        })
    # Si la pagina envia un metodo POST se sigue la logica para iniciar sesion
    else:
        #Recolectamos los datos enviamos por el metodo POST
        username = request.POST['username']
        password = request.POST['password']
        #Con la funcion authenticate vericamos si existe el usuario con esa contrasena
        user = authenticate(request,username=username,password=password)
        # Si el usuario esta vacio se envia un error y se renderiza la pagina 
        if user is None:
            return render(request,'user/login_crud.html',{
                'form':AuthenticationForm,
                'error': 'Username or password is incorrect'
                })
        # Si se encuentra el usaurio pasamos el login que autentica el usuario pasandole como argumento el usuario encontrado
        else:
            login(request,user)
            return redirect('tasks_crud')

# Este decorador nos ayuda a que si el usuario no esta logeado en la pagina, no lo deje accesar
# Y automaticamente lo mande a la pagina de registro de usuario
@login_required
#lo que hace esta funcion es cerrar la sesion del usuario y redireccionarlo al home del crud
def signout(request):
    logout(request)
    return redirect('home_crud')

@login_required
#Muestra las tareas que hay en la base de datos, filtrando por las que hizo el usuario logeado, 
# Y por las que aun no tienen fecha de completadas (task pending)
def tasks(request):
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'tasks/tasks_crud.html',{
        'tasks':tasks
    })


@login_required
#Muestra las tareas que hay en la base de datos, filtrando por las que hizo el usuario logeado, 
# Y por las que  tienen fecha de completadas (task completed)
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'tasks/tasks_crud.html',{
        'tasks':tasks
    })

@login_required
# creamos las tareas
def create_task(request):
    #Creamos nuestro form en forms.py
    task_form = TaskForm()
    # si el metodo es get renderizamos la pagina
    if request.method == 'GET':
        return render(request,'tasks/create_task_crud.html',{
            'form':task_form
        })
    # si es metodo es post hacemos la logica para crear la tarea
    elif request.method == 'POST':
        #task create
        try:
            #recojemos la informacion del formulario
            form = TaskForm(request.POST)
            #creamos la nueva tarea y la guardamos
            new_task = form.save(commit=False)
            #le asigmos el usuario logeado
            new_task.user = request.user
            #guardamos la tarea
            new_task.save()
            return redirect('tasks_crud')
        # manejamos un error por si falla
        except ValueError:
            return render(request,'tasks/create_task_crud.html',{
            'form':task_form,
            'error':'please provide valid data'
        })

@login_required
#mostramos los detalles de la tarea
def task_detail(request,task_id):
    #busamos la tarea por id y por usuario
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    #rellenamos el formulario pasando como parametro la tarea seleeccionada por el usuario
    form = TaskForm(instance=task)

    if request.method == 'GET':
        return render(request,'tasks/task_detail_crud.html',{
            'task':task,
            'form':form,
        })
    elif request.method == 'POST':
        try:
            #busamos la tarea por id y por usuario
            task = get_object_or_404(Task,pk=task_id,user=request.user)
            #rellenamos el formulario pasando como parametro la tarea seleeccionada por el usuario
            form = TaskForm(request.POST,instance=task)
            #guardamos la tarea
            form.save()
            return redirect('tasks_crud')
        #manejamos error en dado caso de no poder guardar la tarea 
        except ValueError:
            return render(request,'tasks/task_detail_crud.html',{
            'task':task,
            'form':form,
            'error':'please provide valid data'
        })

@login_required
#mandamos las tareas no completadas al area de tareas completadas
def task_complete(request,task_id):
    #buscamos la tarea por id y por usuario
    task = get_object_or_404(Task,pk=task_id,user= request.user)
    if request.method == 'POST':
        #le agregmos la fecha de completado
        task.datecompleted = timezone.now()
        #guardamos esa tarea
        task.save()
        return redirect('tasks_crud')

@login_required  
#eliminamos tareas
def task_delete(request,task_id):
    #buscamos la tarea por id y por usuario
    task = get_object_or_404(Task,pk=task_id,user= request.user)
    if request.method == 'POST':
        #con la funcion delete eliminamos la tarea encontrada
        task.delete()
        return redirect('tasks_crud')

