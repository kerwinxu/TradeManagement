from typing_extensions import ParamSpecArgs
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Product, ProductAttribute, ProductAttributeValue, ProductCategory, ProductImage

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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeValueInline, ProductImageInline]
    # 我要可以多种筛选
    list_filter = ('category', 'contact')

