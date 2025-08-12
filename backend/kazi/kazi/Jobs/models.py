from django.db import models
# from users.models import User
import uuid
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from django.urls import reverse_lazy

User = get_user_model()

# Create your models here.
# model for categories


class JobCategories(models.Model):
    update_user = models.ForeignKey(User, related_name="cat_user", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    slug = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = "JobCategory"
        verbose_name_plural = "JobCategories"
    
    def __str__(self):
        return self.title
    
# model for categories_tags


class JobTag(models.Model):
    update_user = models.ForeignKey(User, related_name="tag_user", on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategories, related_name="cat_tag", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    slug = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = "JobTag"
        verbose_name_plural = "JobTags"
        unique_together = ('category','title')
    
    def __str__(self):
        return f"{self.title}-{self.category.title}"
    
# a model for job statues


class JobStatus(models.Model):
    update_user = models.ForeignKey(User, related_name="status_user", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    slug = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()  
    ind_active = models.BooleanField(default=True) 

    class Meta:
        verbose_name = "JobStatus"
        verbose_name_plural = "JobStatuses"
    
    def __str__(self):
        return self.title
    
# a model for jobs


class Job(models.Model):
    update_user = models.ForeignKey(User, related_name="job_owner", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    job_reference = models.CharField( _("reference"), unique=True, editable=False, max_length=10)#  unique refernce to a job not the primary key
    title = models.CharField( _("Title"), max_length=100)
    slug = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(JobCategories, related_name="job_cat", on_delete=models.CASCADE)
    status = models.ForeignKey(JobStatus, related_name="job_status", on_delete=models.CASCADE) # defaults to open automatically
    tags = TaggableManager()
    description = models.TextField()
    preferred_date = models.DateField()
    preferred_time = models.TimeField(null=True, blank=True)
    county = models.CharField(_("County"), max_length=30)
    city = models.CharField(_("city"), max_length=30)
    location = models.CharField(_("location"), max_length=30)
    address = models.CharField(_("Address"), max_length=30)
    latitude = models.DecimalField(max_digits=10,decimal_places=6,null=True,blank=True)
    longitude = models.DecimalField(max_digits=10,decimal_places=6,null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    ind_active = models.BooleanField(default=True) 

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        ordering = ['-create_date']

    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse_lazy("Jobs:job-detail", kwargs={"slug": self.slug})
    




# a model for job images


class JobImage(models.Model):
    update_user = models.ForeignKey(User, related_name="image_user", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    job = models.ForeignKey(Job, verbose_name=_(""), on_delete=models.CASCADE)
    files = models.FileField(blank=True, null=True, upload_to="jobs/files")

    class Meta:
        verbose_name = "JobImage"
        verbose_name_plural = "JobImages"
        ordering = ['-create_date']

    def __str__(self):
        return self.job.title
    
# a model for bookmarks
# a model for rating/review
# a model for complaints