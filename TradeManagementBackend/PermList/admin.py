from django.contrib import admin
from django.http.request import HttpRequest
from PermList.models import PermissionList
from guardian.admin import GuardedModelAdmin
from TradeManagementBackend.GuardedModelAdminBase import GuardedModelAdminBase
from guardian.shortcuts import assign_perm, get_objects_for_user

# Register your models here.

class PermissionListAdmin(GuardedModelAdminBase):
    # 要显示的字段
    list_display = ('source_user', 'next_user')
    # 可以过滤的字段
    list_filter = ('source_user', 'next_user')
 

admin.site.register(PermissionList, PermissionListAdmin)

