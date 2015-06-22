from django.contrib import admin

#jfrom .models import VirtualMachine

class VMAdmin(admin.ModelAdmin):
    fieldsets = [(None, { 'fields': ['name', 'uuid', 'user'] })]
    list_display = ('uuid', 'user')
    list_filter = ['user']

#admin.site.register(VirtualMachine, VMAdmin)
