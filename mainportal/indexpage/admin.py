from django.contrib import admin

from .models import Order, Orgs, Procedures, Marketplaces, Laws, Stages, Tradeplaces, TypesProc


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','partner', 'subj_proc', 'end_date', 'actual_for_me']

@admin.register(Procedures)
class ProceduresAdmin(admin.ModelAdmin):
    list_display = ['id','proc_number', 'subject', 'date_start', 'stage']

@admin.register(Orgs)
class ProceduresAdmin(admin.ModelAdmin):
    list_display = ['id','short_name', 'full_name']

@admin.register(Marketplaces)
class ProceduresAdmin(admin.ModelAdmin):
    list_display = ['id','full_name']

@admin.register(Laws)
class ProceduresAdmin(admin.ModelAdmin):
    list_display = ['id','full_name']

@admin.register(Stages)
class ProceduresAdmin(admin.ModelAdmin):
    list_display = ['id','full_name']

@admin.register(Tradeplaces)
class ProceduresAdmin(admin.ModelAdmin):
    list_display = ['id','full_name']

@admin.register(TypesProc)
class ProceduresAdmin(admin.ModelAdmin):
    list_display = ['id','full_name']

# # Register your models here.
# admin.site.register(Order, OrderAdmin)
