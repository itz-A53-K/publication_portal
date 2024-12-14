from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Department)
class Department(admin.ModelAdmin):
        list_display = ['name', 'abbreviation', 'publication_count']

@admin.register(models.Faculty)
class Faculty(admin.ModelAdmin):
        list_display = ['fid', 'email', 'name', 'is_admin', 'is_superAdmin']

admin.site.register(models.Faculty_details)

@admin.register(models.Article)
class Article(admin.ModelAdmin):
        list_display = ['id', 'title']

@admin.register(models.Book)
class Book(admin.ModelAdmin):
        list_display = ['id', 'title']

@admin.register(models.Citation)
class Citation(admin.ModelAdmin):
        list_display = ['id', 'publication', 'cited_by']
