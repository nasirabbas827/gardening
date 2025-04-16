from django.contrib import admin
from .models import UserRegister , Plant , UserPlant, Profile , Recommendation , Reminder
from .models import Notification , GroupMember , GardeningGroup , Discussion , Resource , GardeningTip



admin.site.register(UserRegister)
admin.site.register(Plant)
admin.site.register(Profile)
admin.site.register(UserPlant)
admin.site.register(Recommendation)
admin.site.register(Reminder)
admin.site.register(Notification)
admin.site.register(GardeningGroup)
admin.site.register(GroupMember)
admin.site.register(Resource)
admin.site.register(GardeningTip)
admin.site.register(Discussion)


