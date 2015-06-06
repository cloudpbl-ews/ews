from django.contrib import admin

from .models import VirtualMachine

class VMAdmin(admin.ModelAdmin):
  # 表示レイアウト
  fieldsets = [(None, { 'fields': ['name', 'uuid', 'user'] })]
  # 表示項目
  list_display = ('uuid', 'user')
  # フィルタ項目
  list_filter = ['user']

admin.site.register(VirtualMachine, VMAdmin)
