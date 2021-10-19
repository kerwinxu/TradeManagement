'''
这个类的作用是，给所有的需要对象权限的类做一个基类，
本文参考 https://lintingbin2009.github.io/2018/10/27/%E4%BD%BF%E7%94%A8django-guardian%E5%AE%9E%E7%8E%B0django-admin%E7%9A%84%E8%A1%8C%E7%BA%A7%E6%9D%83%E9%99%90%E6%8E%A7%E5%88%B6/
'''

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.http.request import HttpRequest
from PermList.models import PermissionList
from django.contrib.auth.models import User

class GuardedModelAdminBase(GuardedModelAdmin):
    """重写了几个方法而已"""

    def get_model_objs(self, request, action=None, klass=None):
        """ 筛选某个用户在某个Mode中中具备权限的数据行（对象）

        Args:
            request ([type]): [连接，里边有属性是某个用户]
            action ([type], optional): [权限]. Defaults to ['view', 'change', 'delete'] . 这个可以是字符串。
            klass ([type], optional): [通常是模板]. Defaults to None.

        Returns:
            [type]: [description]
        """
        opts = self.opts # 实例吧
        klass = klass if klass else opts.model # 示例
        model_name = opts.model_name # 类名
        actions = [action] if action else ['view', 'change', 'delete'] # 权限
        result = get_objects_for_user(
            user=request.user, 
            perms=[f'{perm}_{model_name}' for perm in actions],
            klass=klass, 
            with_superuser=request.user.is_superuser, # 这个十分重要，是否是管理员，默认这个为True的。
            any_perm=True)

        # 调用这个就返回了筛选后的数据行了,这个查询的三要素，用户、模块、权限
        return result
    
    # 在显示数据列表额时候，哪些数据显示，哪些不显示，由该函数控制
    def get_queryset(self, request: HttpRequest):
        """ 返回可以显示的数据，判断依据是，如果是超级管理员，就用

        Args:
            request (HttpRequest): 连接

        Returns:
            可以显示的数据
        """
        if request.user.is_superuser:
            return super().get_queryset(request)
        return self.get_model_objs(request)
    
    def has_perm(self, request, obj, action)->bool:
        """ 判断某个用户对某个对象是否有某个权限

        Args:
            request ([type]): 连接，里边有属性是用户
            obj ([type]): 对象
            action ([type]): 权限

        Returns:
            bool: [description]
        """
        if request.user.is_superuser:
            # 这个首先要判断是否是管理员，
            return True
        opts = self.opts
        codename = f'{action}_{opts.model_name}'
        if obj:
            # 如果有对象，就判断对象权限。
            return request.user.has_perm(f'{opts.app_label}.{codename}', obj)
        else:
            # 其他情况，判断模块权限。
            return self.get_model_objs(request, action).exists()

    def has_change_permission(self, request: HttpRequest,  obj=...) -> bool:
        """是否有修改某个数据行的权限。

        Args:
            request (HttpRequest): 连接，里边有属性是用户
            obj ([type], optional): [description]. Defaults to ....

        Returns:
            bool: [description]
        """
        return self.has_perm(request, obj, 'change')
    
    def has_view_permission(self, request: HttpRequest, obj=None)-> bool:
        """是否有查看某个数据行的权限

        Args:
            request (HttpRequest): 连接，里边有属性是用户
            obj ([type], optional): [description]. Defaults to None.

        Returns:
            bool: [description]
        """
        return self.has_perm(request, obj, 'view')
    
    def has_delete_permission(self, request: HttpRequest, obj=None)-> bool:
        """是否有删除某个数据行的权限

        Args:
            request (HttpRequest): 连接，里边有属性是用户
            obj ([type], optional): [description]. Defaults to None.

        Returns:
            bool: [description]
        """
        return self.has_perm(request, obj, 'delete')
    
    def has_module_permission(self, request: HttpRequest)->bool:
        """模块是否显示，

        Args:
            request (HttpRequest): [description]

        Returns:
            bool: [description]
        """
        if super().has_module_permission(request):
            return True
        try:
            return self.get_model_objs(request).exists()
        except:
            return False
    
    def batch_perm(self,user, obj, actions:list=['view', 'add', 'change', 'delete']):
        """批量的设置某个权限

        Args:
            request (HttpRequest): [description]
            obj ([type]): [description]
            actions (list, optional): [description]. Defaults to ['view', 'add', 'change', 'delete'].
        """
        opts = self.opts
        [assign_perm(f'{opts.app_label}.{action}_{opts.model_name}', user, obj) for action in actions]

    
    def save_model(self, request: HttpRequest, obj, form, change):
        """用户新增应该拥有所有的对象权限。

        Args:
            request (HttpRequest): [description]
            obj ([type]): [description]
            form ([type]): [description]
            change ([type]): [description]

        Returns:
            [type]: [description]
        """
        result = super().save_model(request, obj, form, change)
        if not request.user.is_superuser and not change: # 不是管理员和新增。
            self.batch_perm(request.user, obj)
        return result

    
class GuardedModelAdminEx(GuardedModelAdminBase):
    """这个是上一个的升级"""

    def save_model(self, request: HttpRequest, obj, form, change):
        result =  super().save_model(request, obj, form, change)
        if not request.user.is_superuser and not change: # 不是管理员和新增。
            # 这里增加权限链表下的用户的所有权限。
            for _user in PermissionList.objects.filter(source_user=request.user).values('next_user'):
                u = User.objects.get(id=_user['next_user'])
                self.batch_perm(u, obj)
        return result
