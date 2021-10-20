from typing_extensions import ParamSpecArgs
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Product, ProductAttribute, ProductAttributeValue, ProductCategory, ProductImage
from django.utils.html import format_html
# Register your models here.

# 一个中小的贸易公司企业，都是要推销产品的，这里所有的都可以修改，也就是全局的。
# 以后看看做一个细分的版本

    

# 然后下边创建几个管理类
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    pass

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    # list_display  = ("value", "image_data") # 很多教程上写的是显示这个，但我电脑上却只用下一个就可以了。
    readonly_fields = ('image_data',)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeValueInline, ProductImageInline]
    # 我要可以多种筛选
    list_filter = ('category', 'contact')

