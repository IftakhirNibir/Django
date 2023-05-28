from django.contrib import admin
from .models import *
from embed_video.admin import AdminVideoMixin
# Register your models here.

admin.site.register(Patient)
admin.site.register(Medicine)
admin.site.register(Order)
admin.site.register(Doctor)
admin.site.register(Contect)
admin.site.register(Discussion)
admin.site.register(DiscussionTopic)
admin.site.register(Message)
admin.site.register(Hospital)
admin.site.register(District)
admin.site.register(Ambudetails)
admin.site.register(Ord)
admin.site.register(BkashPayment)
admin.site.register(FS)



class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Item, MyModelAdmin)