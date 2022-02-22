from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','partner', 'subj_proc', 'end_date', 'actual_for_me']

# # Register your models here.
# admin.site.register(Order, OrderAdmin)
