from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('my-plants/', views.my_plants, name='my_plants'),
    path('observations/<int:user_plant_id>/', views.view_observations, name='view_observations'),
    path('reminders/<int:user_plant_id>/', views.view_reminders, name='view_reminders'),
    path('supervisor-dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('recommendations/<int:user_plant_id>/', views.manage_recommendations, name='manage_recommendations'),
    path('recommendations/delete/<int:recommendation_id>/<int:user_plant_id>/', views.delete_recommendation, name='delete_recommendation'), 
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/edit/', views.edit_group, name='edit_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('groups/join/<int:group_id>/', views.join_group, name='join_group'),
    path('groups/leave/<int:group_id>/', views.leave_group, name='leave_group'),
    path('groups/discussions/<int:group_id>/', views.view_discussions, name='view_discussions'),
    path('resources/', views.resource_list, name='resource_list'),  # View all resources
    path('resources/<int:resource_id>/', views.view_resource, name='view_resource'),  # View detailed resource


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
