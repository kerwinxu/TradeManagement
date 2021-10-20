from django.db import models
from Contacts.models import Contacts
from django.utils.html import format_html

# Create your models here.

class ProductCategory(models.Model):
    """产品类别类"""
    category_name = models.CharField(verbose_name="产品类别", max_length=50)
    class Meta:
        verbose_name = '产品类别' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称
    def __str__(self) -> str:
        return self.category_name

class ProductAttribute(models.Model):
    """产品属性类"""
    attribute_name = models.CharField(verbose_name="属性名称", max_length=50)
    category = models.ForeignKey(ProductCategory,  on_delete=models.CASCADE, related_name="attributes")

    class Meta:
        verbose_name = '产品属性' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称
    def __str__(self) -> str:
        return "{}-{}".format(self.category, self.attribute_name)

class Product(models.Model):
    """产品类"""
    product_name = models.CharField(verbose_name="产品名称", max_length=100)
    product_style = models.CharField(verbose_name="产品款号", max_length=100, null=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE, verbose_name="类别")
    contact = models.ForeignKey(Contacts,on_delete=models.CASCADE,blank=True,null=True, verbose_name="联系人")

    class Meta:
        verbose_name = '产品' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称
    
    def __str__(self) -> str:
        return "{}-{}".format(self.product_name, self.product_style)


class ProductAttributeValue(models.Model):
    """产品属性值表"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # 产品
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(verbose_name="属性值",max_length=50)

    class Meta:
        verbose_name = '产品属性值' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称

    def __str__(self) -> str:
        return "{}-{}-{}".format(self.product, self.attribute, self.value)

class ProductImage(models.Model):
    """产品图片类"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # 产品
    value = models.ImageField(upload_to='photos/%Y/%m/%d', max_length=200)

    def image_data(self):
        if self.value:
            return format_html(
                '<img src="{}" width="100px" height="100px"/>',
                self.value.url)
        else:
            return "没有图片"

    image_data.short_description = '图片'
    
    class Meta:
        verbose_name = '产品图片' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称
    
    def __str__(self) -> str:
        return "{}-{}".format(self.product, self.value)
