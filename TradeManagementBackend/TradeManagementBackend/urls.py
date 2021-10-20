"""TradeManagementBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.admin.sites import site
from django.urls import path

from PermList import urls
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',admin.site.urls), # 默认专业也是这个。
    path('admin/', admin.site.urls),
]
# 添加静态的资源目录
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "中小贸易公司管理系统"
admin.site.site_title = "欢迎找我来开发各类中小企业管理系统，淘宝：鑫意雅"
admin.site.index_title = "中小贸易公司管理系统"

