from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# Create your views here.

class PermissionList(models.Model):
    """权限链表，比如一个业务员新增了一个订单，"""
    id = models.AutoField(primary_key=True)
    source_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='用户', related_name='next_user')
    next_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='上级用户', related_name='source_user')

    def __str__(self) -> str:
        return '用户{}拥有用户{}的所有对象权限'.format(self.next_user, self.source_user)
        # return super().__str__()
    
    class Meta:
        verbose_name = '权限列表' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称