from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(CustomUser)


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','created','status']
    list_editable = ['status']
    
    search_fields =['title']
    
   

admin.site.register(post,PostAdmin)
