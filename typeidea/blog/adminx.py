
# from django.contrib import admin
import xadmin
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
from django.contrib.admin.models import LogEntry
from .models import Post, Tag, Category
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.utils.html import format_html
from django.urls import reverse


# Register your models here.

# # 添加日志操作
# @admin.site.register(LogEntry)
# class LogEntryAdmin:
#     list_display = (
#         'object_repr', 'object_id', 'action_flag', 'user', 'change_message'
#     )
#

# 分类页面编辑文章
# class PostInline(admin.TabularInline):
#
#     fields = ('title', 'desc')
#     extra = 1
#     model = Post
class PostInline:
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 1  # 控制额外多几个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline,]
    list_display = ('name', 'status', 'is_nav', 'post_count', 'created_time')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin,self).save_model(request, obj, form, change)


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')

manager.register(CategoryOwnerFilter, take_priority=True)


    # title = '分类过滤器'
    # parameter_name = 'owner_category'
    #
    # def lookups(self, request, model_admin):
    #     return Category.objects.filter(owner=request.user).values_list('id','name')
    #
    # def queryset(self, request, queryset):
    #     category_id = self.value()
    #     if category_id:
    #         return queryset.filter(category_id=self.value())
    #     return queryset


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    # 列表页
    list_display = ('title', 'status', 'category', 'created_time', 'operator')
    list_display_links = []
    list_filter = ['category']
    search_fields = ['title', 'category__name']

    # actions_on_bottom = True
    actions_on_top = True

    # 编辑页
    save_on_top = True

    # fields = (
    #     ('title', 'category'),
    #     'desc',
    #     'content',
    #     'tag',
    # )
    exclude = ['owner']
    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )
    # filter_horizontal = ('tag', )
    # filter_vertical = ('tag', )

    # 自定义字段方法
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


























