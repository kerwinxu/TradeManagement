from django.db import models


class Company(models.Model):
    company_name = models.CharField(verbose_name="公司名称",max_length=20) 
    address = models.CharField(verbose_name="地址",max_length=200, null=True,blank=True)
    phone = models.CharField(verbose_name="电话号码", max_length=50, null=True,blank=True)
    webside = models.URLField(verbose_name="网站", max_length=100, null=True,blank=True)

    class Meta:
        verbose_name = '公司' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称
    def __str__(self) -> str:
        return self.company_name


# Create your models here.
class Contact(models.Model):
    """联系人"""
    # 我这个是中国式的联系人，只有一个姓名
    chinese_name = models.CharField(verbose_name="姓名", max_length=10) 
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING, verbose_name="公司", null=True,blank=True)
    job = models.CharField(verbose_name="职务", max_length=20, null=True,blank=True)
    address = models.CharField(verbose_name="地址",max_length=200, null=True,blank=True)
    phone = models.CharField(verbose_name="电话号码", max_length=50, null=True,blank=True)
    mobile_phone = models.CharField(verbose_name="手机号码", max_length=50, null=True,blank=True)
    email = models.EmailField(verbose_name="Email")
    remark = models.CharField(verbose_name="备注",max_length=200, null=True,blank=True)

    class Meta:
        verbose_name = '联系人' # 单个对象的名称
        verbose_name_plural = verbose_name # 复数对象名称 

    def __str__(self) -> str:
        return "{}:{}".format(self.company, self.chinese_name)

