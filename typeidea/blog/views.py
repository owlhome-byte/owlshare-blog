from pprint import pprint

from datetime import date
from django.core.cache import cache
from django.db.models import F
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from comment.forms import CommentForm
from comment.models import Comment
from .models import Post, Tag, Category
from config.models import SideBar

# Create your views here.


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars':SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category':category
        })

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag':tag
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s'%(uid, self.request.path)
        uv_key = 'uv:%s:%s:%s'%(uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(pv_key, 1, 24*60*60)

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') +1, uv=F('uv')+1)

        if increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv')+1)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword','')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        print(keyword)
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | (Q(desc__icontains=keyword)))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


















#
#
#
# def post_list(request, category_id=None, tag_id=None):
#     print(tag_id)
#     tag = None
#     category = None
#
#     if tag_id:
#         try:
#             tag = Tag.objects.get(id=tag_id)
#         except Exception as e:
#             post_list = []
#         else:
#             post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
#
#     else:
#         post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#         if category_id:
#             try:
#                 category = Category.objects.get(id=category_id)
#             except Exception as e:
#                 category =None
#             post_list = post_list.filter(category_id=category_id)
#     print(post_list)
#     context = {
#         'tag': tag,
#         'category': category,
#         'post_list':post_list,
#         'sidebars':SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#
#     return render(request, 'blog/list.html', context=context)
#
#
# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Exception as e:
#         print(e)
#         post = None
#     context = {
#         'post':post,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)
