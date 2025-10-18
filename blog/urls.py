from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.render_posts,name='posts'),
    path('<int:post_id>',views.post_detail,name='post_detail'),
    
]