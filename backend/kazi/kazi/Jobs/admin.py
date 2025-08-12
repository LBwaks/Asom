from django.contrib import admin
from .models import JobCategories, JobTag, JobStatus, Job, JobImage
# Register your models here.


@admin.register(JobCategories)
class JobCategoriesAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "is_published", "is_featured")
    readonly_fields = ("update_user", "slug")

    def save_model(self, request, obj, form, change):
        if not obj.update_user_id:
            obj.update_user = request.user
            obj.save()
        return super().save_model(request, obj, form, change)
    

@admin.register(JobTag)
class JobTagAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "description", "is_published", "is_featured")
    readonly_fields = ("update_user", "slug")

    def save_model(self, request, obj, form, change):
        if not obj.update_user_id:
            obj.update_user = request.user
            obj.save()
        return super().save_model(request, obj, form, change)
    
    
@admin.register(JobStatus)
class JobStatusAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "ind_active")
    readonly_fields = ("update_user", "slug")
    
    def save_model(self, request, obj, form, change):
        if not obj.update_user_id:
            obj.update_user = request.user
            obj.save()
        return super().save_model(request, obj, form, change)
    

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "ind_active")
    readonly_fields = ("update_user", "slug")

    def save_model(self, request, obj, form, change):
        if not obj.update_user_id:
            obj.update_user = request.user
            obj.save()
        return super().save_model(request, obj, form, change)
    

@admin.register(JobImage)
class JobImages(admin.ModelAdmin):
    list_display = ("job", "files")
    readonly_fields = ("update_user", "slug")

    def save_model(self, request, obj, form, change):
        if not obj.update_user_id:
            obj.update_user = request.user
            obj.save()
        return super().save_model(request, obj, form, change)
    
