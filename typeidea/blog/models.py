from django.contrib.auth.models import User
from django.utils.functional import cached_property
from django.db import models
import mistune

# Create your models here.


class Category(models.Model):
    """
    分类模板
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    is_nav = models.BooleanField(default=False,verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categorys = cls.objects.filter(status=Post.STATUS_NORMAL)
        nav_categorys = []
        normal_categorys = []
        for cate in categorys:
            if cate.is_nav:
                nav_categorys.append(cate)
            else:
                normal_categorys.append(cate)

        return {
            'navs':nav_categorys,
            'categories':normal_categorys,
        }


class Tag(models.Model):
    """
    标签模板
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章模板
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=150, verbose_name='标题')
    desc = models.CharField(max_length=150, verbose_name='概要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    category = models.ForeignKey(Category, verbose_name='分类')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    content_html = models.TextField(verbose_name='正文html代码', blank=True, editable=False)

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    is_md = models.BooleanField(default=False, verbose_name='markdown语法')

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title

    def save(self,  *args, **kwargs):
        # self.content_html = mistune.markdown(self.content)
        # super().save(*args, **kwargs)
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            self.content_html = self.content
        super().save(*args, **kwargs)

    @cached_property
    def get(self):
        return ','.join(self.tag.values_list('name', flat=True))



    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).only('id', 'title').order_by('-pv')

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

























