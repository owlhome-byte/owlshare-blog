from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = '海子博客'
    site_title = '海子的管理后台'
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')