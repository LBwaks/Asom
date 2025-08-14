from rest_framework import serializers
from typing import List
from django.core.exceptions import ValidationError
from .models import JobCategories, JobTag, JobStatus, Job, JobImage
from django.contrib.auth import get_user_model 
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

User = get_user_model()

# Job categories serialers


class JobCategoriesSerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = JobCategories
        fields = ["title", "description", "is_published", "is_featured"]


class JobTagSerializers(serializers.HyperlinkedModelSerializer):
   # category = serializers.HyperlinkedRelatedField(view_name="job-categories", lookup_field="slug", queryset=JobCategories.objects.all())
    
    class Meta:
        model = JobTag
        fields = [#"category", 
                  "title", "description", "is_published", "is_featured"]


class JobStatusSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = JobStatus
        fields = ["title", "description"]


class JobImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JobImage
        fiels = ["files", 'job']


class JobSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    job_url = serializers.HyperlinkedIdentityField(view_name="job-detail", lookup_field="slug")
    # update_user = serializers.HyperlinkedRelatedField(view_name="user-detail", lookup_field="username", queryset=User.objects.all())
    category = serializers.HyperlinkedRelatedField(view_name='job-category-detail', lookup_field="slug", queryset=JobCategories.objects.all())
    status = serializers.HyperlinkedRelatedField(view_name='job-status-detail', lookup_field="slug", queryset=JobStatus.objects.all())
    tags = tags = TagListSerializerField()
    files = JobImageSerializer(many=True, required=False)
    job_files = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False), write_only=True, required=False)
    delete_images_id = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Job
        fields = ["job_url", 
                  "create_date", "update_date", "job_reference", #"update_user", 
                  "title", 
                  "category",
                   "status", "tags",
                    "description", "preferred_date", 
                  "preferred_time", "county", "city", "location", "address", "latitude", "longitude", "files", 
                  "job_files", "delete_images_id",
                  "price", "is_published", "is_featured", "ind_active"]
        
        # --- Policy knobs ---    
        
        MAX_PER_REQUEST = 8            # max files per upload request
        MAX_TOTAL_IMAGES = 20          # max images attached to a product
        MAX_SIZE_MB = 8                # per-file size cap        
        
        def validate_job_files(self, files: List) -> List:                    

            if len(files) > self.MAX_PER_REQUEST:
                raise ValidationError(f"{self.MAX_PER_REQUEST} files/images can only uploaded per request ")
            
            for f in files:
                if f.size > self.MAX_SIZE_MB * 1024 * 1024:
                    raise ValidationError(f"'{getattr(f, 'name', 'file')}' exceecs {self.MAX_SIZE_MB} MB.")
            return files        
        
        def _validate_total_images_cap(self, instance: Job | None, incoming_count: int, delete_count: int):
            # Current count if instance exists
            current = instance.files.count() if instance else 0
            projected = current - delete_count + incoming_count
            if projected < 0:
                projected = 0
            if projected > self.MAX_TOTAL_IMAGES:
                raise ValidationError(
                    f"Too many files. This change would bring the job to {projected} files "
                    f"(cap is {self.MAX_TOTAL_IMAGES})."
                )
            
        def create(self, validated_data):
            job_files = validated_data.pop("job_files", [])
            job = Job.objects.create(**validated_data)
            self.save_files(job, job_files)
            return job
        
        def update(self, instance, validated_data):
            job_files = validated_data.pop("job_files", [])
            delete_images_id = validated_data.pop("delete_images_id", [])

            # update job fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                instance.save()

            # delete selected images
            if delete_images_id:
                JobImage.objects.filter(job=instance, id__in=delete_images_id).delete()
            
            # save new images
            self.save_files(instance, job_files)

            return instance
        
        def save_files(self, job, job_files):

            for file in job_files:
                JobImage.objects.create(job=job, update_user=self.request.user, files=file)


