from django.db import models
from Contacts.models import Company, Contact
from Products.models import Product

# Create your models here.
class Order(models.Model):
    date = models.DateField(verbose_name="日期")
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING) # 联系人
    order_no = models.CharField(verbose_name="合同号码", max_length=200) # 合同号码
    finish = models.BooleanField(verbose_name="完结")

    class Meta:
        verbose_name = '订单' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称
    def __str__(self) -> str:
        return f"日期：{self.date}，联系人：{self.contact}，合同号：{self.order_no}，完结:{self.finish}"


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE, verbose_name="合同") # 合同
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name="产品") # 产品
    num = models.IntegerField(verbose_name="数量")
    finish = models.BooleanField(verbose_name="完结")

    def last_progress(self):
        # 返回最新的一个进展
        return OrderItem.objects.latest()

    last_progress.short_description = "最新进展"

    class Meta:
        verbose_name = '订单项目' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称
    def __str__(self) -> str:
        return f"合同：{self.order},产品：{self.product},数量：{self.num},完结：{self.finish}"


class OrderItemState(models.Model):
    state = models.CharField(verbose_name="状态", max_length=10)

    class Meta:
        verbose_name = '订单状态' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称
    def __str__(self) -> str:
        return self.state

class OrderItemProgress(models.Model):
    date = models.DateField(verbose_name="日期")
    order_item = models.ForeignKey(OrderItem,on_delete=models.CASCADE) 
    order_item_state = models.ForeignKey(OrderItemState, on_delete=models.DO_NOTHING)
    progress = models.CharField(verbose_name="进展", max_length=100)

    class Meta:
        verbose_name = '订单项目进展' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称
    def __str__(self) -> str:
        return f"日期：{self.date},订单项目：{self.order_item},状态：{self.order_item_state}"