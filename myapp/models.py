from django.db import models

class UserRegister(models.Model):
    ROLE_CHOICES = [
        ('Gardener', 'Gardener'),
        ('Supervisor', 'Supervisor'),
        ('HomeOwner', 'HomeOwner'),
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    location = models.CharField(max_length=100, null=True, blank=True)
    climate = models.CharField(max_length=50, null=True, blank=True)
    soil_type = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


from django.db import models

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserRegister, on_delete=models.CASCADE)  # Foreign key reference
    full_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gardening_preferences = models.TextField(null=True, blank=True)  # Store user preferences
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name



class Plant(models.Model):
    CATEGORY_CHOICES = [
        ('Flower', 'Flower'),
        ('Vegetable', 'Vegetable'),
        ('Fruit', 'Fruit'),
    ]

    plant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    characteristics = models.TextField()  # Sun exposure, water needs, etc.
    care_requirements = models.TextField()  # Watering frequency, fertilization, etc.
    age = models.IntegerField(help_text="Age in weeks or months")  # Stores plant age
    growth_stages = models.TextField()  # Different growth phases
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserPlant(models.Model):
    user_plant_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)  # Link to User
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)  # Link to Plant
    date_added = models.DateField(auto_now_add=True)  # Date when the user added the plant
    current_growth_stage = models.CharField(max_length=100)  # Track growth stage
    health_status = models.CharField(max_length=100, choices=[
        ('Healthy', 'Healthy'),
        ('Needs Attention', 'Needs Attention'),
        ('Wilting', 'Wilting'),
        ('Diseased', 'Diseased'),
    ])
    notes = models.TextField(null=True, blank=True)  # Optional user notes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.plant.name}"


from django.db import models
from django.contrib.auth.models import User

class Observation(models.Model):
    observation_id = models.AutoField(primary_key=True)
    user_plant = models.ForeignKey('UserPlant', on_delete=models.CASCADE)  # Link to User's Plant
    observation_date = models.DateField(auto_now_add=True)
    growth_stage = models.CharField(max_length=100)  # Stage of growth
    health_indicator = models.CharField(max_length=100, choices=[
        ('Healthy', 'Healthy'),
        ('Diseased', 'Diseased'),
        ('Wilting', 'Wilting'),
        ('Needs Attention', 'Needs Attention'),
    ])
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Observation on {self.observation_date} - {self.user_plant.plant.name}"

class Reminder(models.Model):
    reminder_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserRegister', on_delete=models.CASCADE)  # Link to User
    user_plant = models.ForeignKey('UserPlant', on_delete=models.CASCADE)  # Link to User's Plant
    task_type = models.CharField(max_length=100, choices=[
        ('Watering', 'Watering'),
        ('Pruning', 'Pruning'),
        ('Repotting', 'Repotting'),
        ('Fertilizing', 'Fertilizing'),
    ])
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reminder: {self.task_type} for {self.user_plant.plant.name} on {self.due_date}"



from django.db import models
from .models import UserRegister, UserPlant

class Recommendation(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    supervisor = models.ForeignKey(UserRegister, on_delete=models.CASCADE, limit_choices_to={'role': 'Supervisor'})  
    user_plant = models.ForeignKey(UserPlant, on_delete=models.CASCADE)  
    watering_schedule = models.TextField()
    fertilization_plan = models.TextField()
    pest_control_measures = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recommendation by {self.supervisor.username} for {self.user_plant.plant.name}"



# Notification System
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE) 
    title = models.CharField(max_length=100)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('Reminder', 'Reminder'),
        ('Alert', 'Alert'),
        ('Community', 'Community'),
        ('System', 'System'),
    ])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} for {self.user.username}"
    

class GardeningGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    social_media_link = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class GroupMember(models.Model):
    member_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(GardeningGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('group', 'user')  # Ensure unique membership per user per group
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


class Discussion(models.Model):
    discussion_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(GardeningGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username} on {self.group.name}: {self.content[:30]}"  # Short preview of the content
    


class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()  # For the full text of the resource (tutorial/article)
    category = models.CharField(max_length=100, choices=[
        ('tutorial', 'Tutorial'),
        ('article', 'Article'),
        ('guide', 'Guide'),
    ])  # To differentiate between the types of educational resources
    video_link = models.URLField(blank=True, null=True)  # Optional link to a related video
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class GardeningTip(models.Model):
    weather_type = models.CharField(max_length=50)  # e.g., 'Rain', 'Clear', 'Snow', 'Clouds'
    tip = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.weather_type} - Tip"
