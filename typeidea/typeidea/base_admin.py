import xadmin

class BaseOwnerAdmin:
    """
    1. 用来处理文章、分类、标签、侧边栏、友链这些model的owner字段自动补充
    2. 用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )

    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()





# class BaseOwnerAdmin:
#     """
#     用来针对query过滤当前用户
#     用来自动补充文章 分类 标签侧边栏这些的owner字段
#     """
#     exclude = ('owner',)
#
#     def get_list_queryset(self):
#         request = self.request
#         qs = super().get_list_queryset()
#         return qs.filter(owner=request.user)
#
#     def save_model(self, request, obj, form, change):
#         # obj.owner = request.user
#         self.new_obj.owner = self.request.user
#         return super().save_models()

