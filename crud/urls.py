from django.urls import path
from crud import views

urlpatterns = [
    
    path('', views.home,name='home_crud'),
    path('signup/',views.signup,name='signup_crud'),
    path('signin/', views.signin, name='signin_crud'),
    path('logout',views.signout,name='logout_crud'),
    path('tasks/',views.tasks,name='tasks_crud'),
    path('tasks_completed/',views.tasks_completed,name='tasks_completed_crud'),
    path('tasks/create', views.create_task, name='task_create_crud'),
    #estas rutas piden un argumento de valor entero (int), que seria el id de la tarea(task_id)
    path('tasks/<int:task_id>', views.task_detail, name='task_detail_crud'),
    path('tasks/<int:task_id>/complete', views.task_complete, name='task_complete_crud'),
    path('tasks/<int:task_id>/delete', views.task_delete, name='task_delete_crud'),
]
