from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, LoginForm , UserUpdateForm
from .models import UserRegister , Profile


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserRegister
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = UserRegister.objects.get(username=username)
                if user.password == password:
                    request.session['username'] = username
                    request.session['user_role'] = user.role  # Store user role in session
                    
                    messages.success(request, 'Login successful!')

                    # Redirect based on user role
                    if user.role == 'Supervisor':
                        return redirect('supervisor_dashboard')  # Redirect to supervisor dashboard
                    else:
                        return redirect('home')  # Redirect normal users to home page
                else:
                    messages.error(request, 'Invalid password.')
            except UserRegister.DoesNotExist:
                messages.error(request, 'Username does not exist.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import UserPlant, Observation, Recommendation

def supervisor_dashboard(request):
    # Ensure only supervisors can access
    if 'username' not in request.session or request.session.get('user_role') != 'Supervisor':
        return redirect('login')  

    # Fetch all user plants and their observations
    user_plants = UserPlant.objects.all()
    observations = Observation.objects.select_related('user_plant').all()

    # Fetch all recommendations for easy access
    recommendations = Recommendation.objects.select_related('user_plant').all()
    

    context = {
        'user_plants': user_plants,
        'observations': observations,
        'recommendations': recommendations,
    }

    return render(request, 'supervisor_dashboard.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserRegister, Plant, UserPlant, Reminder, Recommendation

from .models import Notification


import requests

def get_weather_data(location):
    api_key = '219ff162a58589430fc465f29dd1d386'  # Replace with your own
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if data.get('cod') != '200':
            return None

        daily_data = {}
        for entry in data['list']:
            date = entry['dt_txt'].split(' ')[0]
            if date not in daily_data:
                daily_data[date] = {
                    'temp': [],
                    'feels_like': [],
                    'pressure': [],
                    'humidity': [],
                    'wind_speed': [],
                    'weather': entry['weather'][0],  # Use first entry for icon/desc
                }
            daily_data[date]['temp'].append(entry['main']['temp'])
            daily_data[date]['feels_like'].append(entry['main']['feels_like'])
            daily_data[date]['pressure'].append(entry['main']['pressure'])
            daily_data[date]['humidity'].append(entry['main']['humidity'])
            daily_data[date]['wind_speed'].append(entry['wind']['speed'])

        summaries = {}
        for date, vals in daily_data.items():
            summaries[date] = {
                'temp': round(sum(vals['temp']) / len(vals['temp']), 1),
                'feels_like': round(sum(vals['feels_like']) / len(vals['feels_like']), 1),
                'pressure': round(sum(vals['pressure']) / len(vals['pressure']), 1),
                'humidity': round(sum(vals['humidity']) / len(vals['humidity']), 1),
                'wind_speed': round(sum(vals['wind_speed']) / len(vals['wind_speed']), 1),
                'weather': vals['weather'],
            }

        return summaries

    except Exception:
        return None


from .models import GardeningTip  # Make sure you’ve imported this at the top

def home(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')

    try:
        user = UserRegister.objects.get(username=username)
    except UserRegister.DoesNotExist:
        return redirect('login')

    plants = Plant.objects.all()
    weather_forecast = get_weather_data(user.location)

    current_weather = None
    gardening_tip = None

    if weather_forecast:
        today = list(weather_forecast.keys())[0]
        current_weather = weather_forecast[today]['weather']['main']  # e.g., 'Rain'

        try:
            gardening_tip = GardeningTip.objects.filter(weather_type__icontains=current_weather).first()
        except:
            gardening_tip = None

    reminders = Reminder.objects.filter(user=user, is_completed=False).order_by('due_date')
    user_plants = UserPlant.objects.filter(user=user)
    recommendations = Recommendation.objects.filter(user_plant__in=user_plants)
    notifications = Notification.objects.filter(user__username=username, is_read=False).order_by('-created_at')
    group_memberships = GroupMember.objects.filter(user=user)
    user_groups = [membership.group for membership in group_memberships]

    if request.method == 'POST':
        plant_id = request.POST.get('plant_id')
        plant = get_object_or_404(Plant, plant_id=plant_id)

        if UserPlant.objects.filter(user=user, plant=plant).exists():
            messages.warning(request, "You have already added this plant.")
        else:
            UserPlant.objects.create(user=user, plant=plant, current_growth_stage="Seedling", health_status="Healthy")
            messages.success(request, "Plant added successfully!")

    context = {
        'username': username,
        'plants': plants,
        'reminders': reminders,
        'recommendations': recommendations,
        'notifications': notifications,
        'user_groups': user_groups,
        'weather_forecast': weather_forecast,
        'current_weather': current_weather,
        'gardening_tip': gardening_tip,
    }

    return render(request, 'home.html', context)



def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserRegister, Profile
from .forms import UserUpdateForm

def update_profile(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user = get_object_or_404(UserRegister, username=username)
    
    # Ensure the profile exists or create it if necessary
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('home')
    else:
        form = UserUpdateForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserRegister, UserPlant, Observation, Reminder

def my_plants(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')

    try:
        user = UserRegister.objects.get(username=username)
    except UserRegister.DoesNotExist:
        return redirect('login')

    user_plants = UserPlant.objects.filter(user=user)  # Fetch plants added by user

    context = {
        'username': username,
        'user_plants': user_plants,
    }
    
    return render(request, 'my_plants.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserPlant, Observation, Reminder
from django.utils import timezone

# View, Add, and Delete Observations
def view_observations(request, user_plant_id):
    user_plant = get_object_or_404(UserPlant, user_plant_id=user_plant_id)
    observations = Observation.objects.filter(user_plant=user_plant)

    # Handle adding a new observation
    if request.method == 'POST' and 'add_observation' in request.POST:
        growth_stage = request.POST.get('growth_stage')
        health_indicator = request.POST.get('health_indicator')
        notes = request.POST.get('notes')

        if growth_stage and health_indicator:
            Observation.objects.create(
                user_plant=user_plant,
                observation_date=timezone.now().date(),
                growth_stage=growth_stage,
                health_indicator=health_indicator,
                notes=notes
            )
            messages.success(request, "Observation added successfully!")
            return redirect('view_observations', user_plant_id=user_plant_id)

    # Handle deletion of an observation
    if request.method == 'POST' and 'delete_observation' in request.POST:
        observation_id = request.POST.get('observation_id')
        observation = get_object_or_404(Observation, observation_id=observation_id)
        observation.delete()
        messages.success(request, "Observation deleted successfully!")
        return redirect('view_observations', user_plant_id=user_plant_id)

    context = {
        'user_plant': user_plant,
        'observations': observations,
    }
    return render(request, 'view_observations.html', context)

# View, Add, and Delete Reminders
def view_reminders(request, user_plant_id):
    user_plant = get_object_or_404(UserPlant, user_plant_id=user_plant_id)
    reminders = Reminder.objects.filter(user_plant=user_plant)

    # Handle adding a new reminder
    if request.method == 'POST' and 'add_reminder' in request.POST:
        task_type = request.POST.get('task_type')
        due_date = request.POST.get('due_date')

        if task_type and due_date:
            Reminder.objects.create(
                user=user_plant.user,
                user_plant=user_plant,
                task_type=task_type,
                due_date=due_date
            )
            messages.success(request, "Reminder added successfully!")
            return redirect('view_reminders', user_plant_id=user_plant_id)

    # Handle deletion of a reminder
    if request.method == 'POST' and 'delete_reminder' in request.POST:
        reminder_id = request.POST.get('reminder_id')
        reminder = get_object_or_404(Reminder, reminder_id=reminder_id)
        reminder.delete()
        messages.success(request, "Reminder deleted successfully!")
        return redirect('view_reminders', user_plant_id=user_plant_id)

    context = {
        'user_plant': user_plant,
        'reminders': reminders,
    }
    return render(request, 'view_reminders.html', context)





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Recommendation, UserPlant, UserRegister
from .forms import RecommendationForm

def manage_recommendations(request, user_plant_id):
    # Ensure only supervisors can access
    if 'username' not in request.session or request.session.get('user_role') != 'Supervisor':
        return redirect('login')  

    user_plant = get_object_or_404(UserPlant, user_plant_id=user_plant_id)
    recommendations = Recommendation.objects.filter(user_plant=user_plant)

    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            supervisor = get_object_or_404(UserRegister, username=request.session['username'])
            recommendation.supervisor = supervisor
            recommendation.user_plant = user_plant
            recommendation.save()
            messages.success(request, "Recommendation added successfully!")
            return redirect('manage_recommendations', user_plant_id=user_plant_id)
    else:
        form = RecommendationForm()

    context = {
        'user_plant': user_plant,
        'recommendations': recommendations,
        'form': form,
    }
    return render(request, 'manage_recommendations.html', context)

def delete_recommendation(request, recommendation_id, user_plant_id):
    recommendation = get_object_or_404(Recommendation, recommendation_id=recommendation_id)
    recommendation.delete()
    messages.success(request, "Recommendation deleted successfully!")
    return redirect('manage_recommendations', user_plant_id=user_plant_id)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import GardeningGroup, UserRegister
from .forms import GardeningGroupForm  # You'll create this form below

from django.shortcuts import render, get_object_or_404, redirect
from .models import GardeningGroup, GroupMember, Discussion
from django.contrib import messages

# Group List View
from django.shortcuts import render, get_object_or_404
from .models import GardeningGroup, GroupMember, UserRegister

def group_list(request):
    # Fetch the logged-in user from the session
    username = request.session.get('username')
    user = get_object_or_404(UserRegister, username=username)
    
    # Get all groups
    groups = GardeningGroup.objects.all()

    # Get the groups the user is a member of
    group_memberships = GroupMember.objects.filter(user=user)
    user_groups = [membership.group for membership in group_memberships]

    return render(request, 'groups/group_list.html', {
        'groups': groups,
        'user_groups': user_groups,
        'user': user,
    })


# Join Group
def join_group(request, group_id):
    username = request.session.get('username')
    user = get_object_or_404(UserRegister, username=username)
    group = get_object_or_404(GardeningGroup, group_id=group_id)

    # Ensure user isn't already a member
    if GroupMember.objects.filter(user=user, group=group).exists():
        messages.warning(request, "You are already a member of this group.")
    else:
        # Create a new group membership
        GroupMember.objects.create(user=user, group=group)
        messages.success(request, "You have successfully joined the group.")
    
    return redirect('group_list')

# Leave Group
def leave_group(request, group_id):
    username = request.session.get('username')
    user = get_object_or_404(UserRegister, username=username)
    group = get_object_or_404(GardeningGroup, group_id=group_id)

    # Ensure the user is a member before leaving
    try:
        membership = GroupMember.objects.get(user=user, group=group)
        membership.delete()
        messages.success(request, "You have left the group.")
    except GroupMember.DoesNotExist:
        messages.warning(request, "You are not a member of this group.")
    
    return redirect('group_list')

from django.shortcuts import render, get_object_or_404, redirect
from .models import GardeningGroup, Discussion, UserRegister

def view_discussions(request, group_id):
    # Get the group
    group = get_object_or_404(GardeningGroup, group_id=group_id)

    # Fetch all discussions for this group, ordered by creation date
    discussions = Discussion.objects.filter(group=group).order_by('-created_at')

    if request.method == 'POST':
        # Retrieve the content of the new discussion message
        content = request.POST.get('content')
        
        if content:
            # Get the user who is posting the message (based on the session username)
            username = request.session.get('username')
            user = get_object_or_404(UserRegister, username=username)
            
            # Create and save the new discussion message
            Discussion.objects.create(group=group, user=user, content=content)
            
            # Redirect back to the same page to display the new message
            return redirect('view_discussions', group_id=group_id)

    # Return the template with the group and its discussions
    return render(request, 'groups/group_discussions.html', {
        'group': group,
        'discussions': discussions
    })


from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import GardeningGroupForm
from .models import GardeningGroup, GroupMember, UserRegister

def create_group(request):
    username = request.session.get('username')
    user = get_object_or_404(UserRegister, username=username)

    if request.method == 'POST':
        form = GardeningGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = user
            group.save()

            # Automatically add the user to the group as a member
            GroupMember.objects.create(group=group, user=user, is_admin=True)

            messages.success(request, "Group created and you have been added to the group.")
            return redirect('group_list')
    else:
        form = GardeningGroupForm()

    return render(request, 'groups/group_form.html', {'form': form, 'title': 'Create Group'})


def edit_group(request, group_id):
    group = get_object_or_404(GardeningGroup, pk=group_id)

    if request.method == 'POST':
        form = GardeningGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group updated successfully.")
            return redirect('group_list')
    else:
        form = GardeningGroupForm(instance=group)

    return render(request, 'groups/group_form.html', {'form': form, 'title': 'Edit Group'})

def delete_group(request, group_id):
    group = get_object_or_404(GardeningGroup, pk=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, "Group deleted successfully.")
        return redirect('group_list')
    return render(request, 'groups/group_confirm_delete.html', {'group': group})


from django.shortcuts import render, get_object_or_404
from .models import Resource

# View to list all resources
def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'resources/resource_list.html', {
        'resources': resources
    })

# View to display a specific resource with a video if available
def view_resource(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    return render(request, 'resources/view_resource.html', {
        'resource': resource
    })
